"""
Heisenbug Demo - Challenge Three: Heisenbugs
=============================================
Demonstrates a race condition (Heisenbug) that appears/disappears
based on execution perturbation using Execution Indexing.

Concept: A bug that changes behavior when you try to observe it.
"""

import threading
import time
from typing import List, Tuple
from execution_indexer import ExecutionPoint


class BankAccount:
    """
    Simple bank account with a race condition bug.
    
    The bug: Non-atomic read-modify-write on balance
    """
    
    def __init__(self, initial_balance: float = 1000.0):
        self.balance = initial_balance
        self.transaction_log: List[str] = []
        self.lock = threading.Lock()  # Available but not used initially
    
    def transfer(self, amount: float, use_lock: bool = False):
        """
        Transfer money (withdraw then deposit simulation).
        
        Args:
            amount: Amount to transfer
            use_lock: Whether to use thread-safe locking
        """
        if use_lock:
            with self.lock:
                self._unsafe_transfer(amount)
        else:
            self._unsafe_transfer(amount)
    
    def _unsafe_transfer(self, amount: float):
        """Unsafe transfer with race condition"""
        # Read balance
        current_balance = self.balance
        
        # Simulate some processing time
        # This is where race condition can occur
        time.sleep(0.0001)  # 0.1ms delay
        
        # Write new balance
        new_balance = current_balance - amount
        self.balance = new_balance
        
        # Log transaction
        thread_name = threading.current_thread().name
        self.transaction_log.append(
            f"{thread_name}: {current_balance} -> {new_balance} (withdrew {amount})"
        )
    
    def get_balance(self) -> float:
        """Get current balance"""
        return self.balance
    
    def print_log(self):
        """Print transaction log"""
        print("\nTransaction Log:")
        for entry in self.transaction_log:
            print(f"  {entry}")


class Perturbator:
    """
    Perturbator that uses Execution Indexing to inject delays
    at specific execution points to trigger race conditions.
    """
    
    def __init__(self):
        self.perturbation_points: List[ExecutionPoint] = []
        self.delay_ms: float = 10.0  # Default 10ms delay
    
    def add_perturbation_point(self, 
                              context: Tuple[str, ...],
                              statement: int,
                              instance: int):
        """
        Add a perturbation point.
        
        Args:
            context: Calling context tuple
            statement: Line number
            instance: Instance number
        """
        point = ExecutionPoint(
            context=context,
            statement=statement,
            instance=instance
        )
        self.perturbation_points.append(point)
    
    def should_perturb(self, current_point: ExecutionPoint) -> bool:
        """Check if we should perturb at this execution point"""
        return current_point in self.perturbation_points
    
    def inject_delay(self):
        """Inject a delay (perturbation)"""
        time.sleep(self.delay_ms / 1000.0)


def run_normal_execution(num_threads: int = 2, amount: float = 100.0) -> BankAccount:
    """
    Run normal execution without perturbation.
    
    This may or may not show the bug depending on timing.
    
    Args:
        num_threads: Number of concurrent threads
        amount: Amount each thread transfers
        
    Returns:
        BankAccount after execution
    """
    account = BankAccount(initial_balance=1000.0)
    threads = []
    
    for i in range(num_threads):
        thread = threading.Thread(
            target=account.transfer,
            args=(amount,),
            name=f"Thread-{i+1}"
        )
        threads.append(thread)
    
    # Start all threads
    for thread in threads:
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    return account


def run_perturbed_execution(num_threads: int = 2, 
                           amount: float = 100.0,
                           perturbation_delay_ms: float = 5.0) -> BankAccount:
    """
    Run execution with perturbation to force race condition.
    
    By injecting a delay at a specific execution point,
    we force a particular thread interleaving that reveals the bug.
    
    Args:
        num_threads: Number of concurrent threads
        amount: Amount each thread transfers
        perturbation_delay_ms: Delay to inject in milliseconds
        
    Returns:
        BankAccount after execution
    """
    account = BankAccount(initial_balance=1000.0)
    
    # Create perturbator
    perturbator = Perturbator()
    perturbator.delay_ms = perturbation_delay_ms
    
    # Add perturbation point: inject delay after reading balance
    # This forces the race condition to occur
    
    def perturbed_transfer(amount: float):
        """Transfer with perturbation injection"""
        # Read balance
        current_balance = account.balance
        
        # PERTURBATION: Inject delay here to force race condition
        time.sleep(perturbation_delay_ms / 1000.0)
        
        # Write new balance
        new_balance = current_balance - amount
        account.balance = new_balance
        
        # Log transaction
        thread_name = threading.current_thread().name
        account.transaction_log.append(
            f"{thread_name}: {current_balance} -> {new_balance} (withdrew {amount})"
        )
    
    threads = []
    
    for i in range(num_threads):
        thread = threading.Thread(
            target=perturbed_transfer,
            args=(amount,),
            name=f"Thread-{i+1}"
        )
        threads.append(thread)
    
    # Start all threads
    for thread in threads:
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    return account


def run_safe_execution(num_threads: int = 2, amount: float = 100.0) -> BankAccount:
    """
    Run execution with proper locking (no bug).
    
    Args:
        num_threads: Number of concurrent threads
        amount: Amount each thread transfers
        
    Returns:
        BankAccount after execution
    """
    account = BankAccount(initial_balance=1000.0)
    threads = []
    
    for i in range(num_threads):
        thread = threading.Thread(
            target=account.transfer,
            args=(amount, True),  # use_lock=True
            name=f"Thread-{i+1}"
        )
        threads.append(thread)
    
    # Start all threads
    for thread in threads:
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    return account


def demonstrate_heisenbug():
    """
    Main demonstration of Heisenbug concept.
    
    Shows three scenarios:
    1. Normal execution (bug may or may not appear)
    2. Perturbed execution (bug forced to appear)
    3. Safe execution with locks (no bug)
    """
    print("\n" + "="*80)
    print("HEISENBUG DEMONSTRATION: Race Condition in Bank Transfer")
    print("="*80)
    
    initial_balance = 1000.0
    num_threads = 3
    amount_per_thread = 100.0
    expected_final_balance = initial_balance - (num_threads * amount_per_thread)
    
    print(f"\nSetup:")
    print(f"  Initial Balance: ${initial_balance}")
    print(f"  Number of Threads: {num_threads}")
    print(f"  Amount per Thread: ${amount_per_thread}")
    print(f"  Expected Final Balance: ${expected_final_balance}")
    
    # Scenario 1: Normal execution
    print("\n" + "-"*80)
    print("SCENARIO 1: Normal Execution (Fast, No Perturbation)")
    print("-"*80)
    
    account1 = run_normal_execution(num_threads, amount_per_thread)
    final_balance1 = account1.get_balance()
    
    print(f"\nFinal Balance: ${final_balance1}")
    print(f"Expected: ${expected_final_balance}")
    
    if abs(final_balance1 - expected_final_balance) < 0.01:
        print("✓ Result: CORRECT (Bug did not manifest)")
    else:
        print("✗ Result: INCORRECT (Bug manifested!)")
        print(f"  Lost: ${expected_final_balance - final_balance1}")
    
    account1.print_log()
    
    # Scenario 2: Perturbed execution
    print("\n" + "-"*80)
    print("SCENARIO 2: Perturbed Execution (Forced Race Condition)")
    print("-"*80)
    print("Injecting delay to force specific thread interleaving...")
    
    account2 = run_perturbed_execution(num_threads, amount_per_thread, 
                                       perturbation_delay_ms=5.0)
    final_balance2 = account2.get_balance()
    
    print(f"\nFinal Balance: ${final_balance2}")
    print(f"Expected: ${expected_final_balance}")
    
    if abs(final_balance2 - expected_final_balance) < 0.01:
        print("✓ Result: CORRECT (Bug did not manifest)")
    else:
        print("✗ Result: INCORRECT (Bug manifested!)")
        print(f"  Lost: ${expected_final_balance - final_balance2}")
    
    account2.print_log()
    
    # Scenario 3: Safe execution with locks
    print("\n" + "-"*80)
    print("SCENARIO 3: Safe Execution (With Thread Locks)")
    print("-"*80)
    
    account3 = run_safe_execution(num_threads, amount_per_thread)
    final_balance3 = account3.get_balance()
    
    print(f"\nFinal Balance: ${final_balance3}")
    print(f"Expected: ${expected_final_balance}")
    
    if abs(final_balance3 - expected_final_balance) < 0.01:
        print("✓ Result: CORRECT (Locks prevent race condition)")
    else:
        print("✗ Result: INCORRECT (Unexpected!)")
    
    account3.print_log()
    
    # Summary
    print("\n" + "="*80)
    print("HEISENBUG ANALYSIS")
    print("="*80)
    print("\nKey Observations:")
    print("1. Normal execution may hide the bug due to fast execution")
    print("2. Perturbation (delay injection) forces the race condition to appear")
    print("3. Proper synchronization (locks) eliminates the bug")
    print("\nThis demonstrates how Heisenbugs can disappear when you try to")
    print("observe them (e.g., with debuggers that slow down execution).")
    print("="*80 + "\n")


# Example usage and testing
if __name__ == "__main__":
    demonstrate_heisenbug()
