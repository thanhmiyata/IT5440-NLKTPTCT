"""
Fault Localization - Concept 4: Spectrum-based Fault Localization
==================================================================
Implements spectrum-based fault localization using Tarantula and Ochiai formulas.
Identifies suspicious lines based on test case pass/fail patterns.
"""

from typing import List, Dict, Tuple, Callable
from dataclasses import dataclass
import math


@dataclass
class TestCase:
    """Represents a single test case"""
    name: str
    input_args: tuple
    expected_output: any
    actual_output: any = None
    passed: bool = False
    covered_lines: set = None
    
    def __post_init__(self):
        if self.covered_lines is None:
            self.covered_lines = set()


@dataclass
class SuspiciousnessScore:
    """Suspiciousness score for a line of code"""
    line_number: int
    tarantula_score: float
    ochiai_score: float
    failed_count: int
    passed_count: int
    
    def __repr__(self):
        return (f"Line {self.line_number}: "
                f"Tarantula={self.tarantula_score:.3f}, "
                f"Ochiai={self.ochiai_score:.3f} "
                f"(failed={self.failed_count}, passed={self.passed_count})")


class FaultLocalizer:
    """
    Fault Localizer using Spectrum-based Fault Localization.
    
    Process:
    1. Run each test case with Tracer
    2. Build Spectra Matrix (tests × lines)
    3. Apply Tarantula/Ochiai formulas
    4. Rank lines by suspiciousness
    """
    
    def __init__(self):
        self.test_cases: List[TestCase] = []
        self.all_lines: set = set()
        self.spectra_matrix: Dict[str, set] = {}  # test_name -> covered_lines
        
    def add_test_case(self, 
                      name: str,
                      input_args: tuple,
                      expected_output: any) -> TestCase:
        """
        Add a test case to the fault localizer.
        
        Args:
            name: Test case name
            input_args: Input arguments for the function
            expected_output: Expected output
            
        Returns:
            TestCase object
        """
        test_case = TestCase(
            name=name,
            input_args=input_args,
            expected_output=expected_output
        )
        self.test_cases.append(test_case)
        return test_case
    
    def run_tests(self, target_function: Callable, use_tracer: bool = True):
        """
        Run all test cases and collect coverage information.
        
        Args:
            target_function: Function to test
            use_tracer: Whether to use Tracer for coverage (default: True)
        """
        if use_tracer:
            from tracer_engine import Tracer
        
        for test_case in self.test_cases:
            try:
                if use_tracer:
                    # Run with tracer to get coverage
                    tracer = Tracer()
                    actual_output = tracer.trace_execution(
                        target_function,
                        *test_case.input_args
                    )
                    
                    # Get covered lines
                    test_case.covered_lines = set(tracer.get_executed_lines())
                    self.all_lines.update(test_case.covered_lines)
                else:
                    # Run without tracer
                    actual_output = target_function(*test_case.input_args)
                
                test_case.actual_output = actual_output
                
                # Check if test passed
                test_case.passed = (actual_output == test_case.expected_output)
                
            except Exception as e:
                test_case.actual_output = f"Exception: {e}"
                test_case.passed = False
            
            # Store in spectra matrix
            self.spectra_matrix[test_case.name] = test_case.covered_lines
    
    def compute_suspiciousness(self) -> List[SuspiciousnessScore]:
        """
        Compute suspiciousness scores for all lines using Tarantula and Ochiai.
        
        Returns:
            List of SuspiciousnessScore objects, sorted by Tarantula score
        """
        # Count total passed and failed tests
        total_failed = sum(1 for tc in self.test_cases if not tc.passed)
        total_passed = sum(1 for tc in self.test_cases if tc.passed)
        
        if total_failed == 0:
            print("Warning: No failed test cases. Cannot compute suspiciousness.")
            return []
        
        suspiciousness_scores = []
        
        for line in sorted(self.all_lines):
            # Count how many failed/passed tests cover this line
            failed_covering = sum(
                1 for tc in self.test_cases 
                if not tc.passed and line in tc.covered_lines
            )
            passed_covering = sum(
                1 for tc in self.test_cases 
                if tc.passed and line in tc.covered_lines
            )
            
            # Tarantula formula
            tarantula_score = self._compute_tarantula(
                failed_covering, total_failed,
                passed_covering, total_passed
            )
            
            # Ochiai formula
            ochiai_score = self._compute_ochiai(
                failed_covering, total_failed,
                passed_covering, total_passed
            )
            
            suspiciousness_scores.append(SuspiciousnessScore(
                line_number=line,
                tarantula_score=tarantula_score,
                ochiai_score=ochiai_score,
                failed_count=failed_covering,
                passed_count=passed_covering
            ))
        
        # Sort by Tarantula score (descending)
        suspiciousness_scores.sort(key=lambda x: x.tarantula_score, reverse=True)
        
        return suspiciousness_scores
    
    def _compute_tarantula(self, 
                          failed_covering: int, 
                          total_failed: int,
                          passed_covering: int, 
                          total_passed: int) -> float:
        """
        Compute Tarantula suspiciousness score.
        
        Formula: failed(s)/total_failed / (passed(s)/total_passed + failed(s)/total_failed)
        
        Args:
            failed_covering: Number of failed tests covering this line
            total_failed: Total number of failed tests
            passed_covering: Number of passed tests covering this line
            total_passed: Total number of passed tests
            
        Returns:
            Tarantula score (0.0 to 1.0)
        """
        if total_failed == 0:
            return 0.0
        
        failed_ratio = failed_covering / total_failed if total_failed > 0 else 0.0
        passed_ratio = passed_covering / total_passed if total_passed > 0 else 0.0
        
        denominator = passed_ratio + failed_ratio
        
        if denominator == 0:
            return 0.0
        
        return failed_ratio / denominator
    
    def _compute_ochiai(self,
                       failed_covering: int,
                       total_failed: int,
                       passed_covering: int,
                       total_passed: int) -> float:
        """
        Compute Ochiai suspiciousness score.
        
        Formula: failed(s) / sqrt(total_failed * (failed(s) + passed(s)))
        
        Args:
            failed_covering: Number of failed tests covering this line
            total_failed: Total number of failed tests
            passed_covering: Number of passed tests covering this line
            total_passed: Total number of passed tests
            
        Returns:
            Ochiai score (0.0 to 1.0)
        """
        if total_failed == 0 or failed_covering == 0:
            return 0.0
        
        total_covering = failed_covering + passed_covering
        
        if total_covering == 0:
            return 0.0
        
        denominator = math.sqrt(total_failed * total_covering)
        
        if denominator == 0:
            return 0.0
        
        return failed_covering / denominator
    
    def print_results(self, top_n: int = 10):
        """
        Print fault localization results.
        
        Args:
            top_n: Number of top suspicious lines to display
        """
        print("\n" + "="*80)
        print("FAULT LOCALIZATION RESULTS")
        print("="*80)
        
        # Print test case summary
        print("\nTest Case Summary:")
        passed_count = sum(1 for tc in self.test_cases if tc.passed)
        failed_count = len(self.test_cases) - passed_count
        print(f"  Total: {len(self.test_cases)} tests")
        print(f"  Passed: {passed_count}")
        print(f"  Failed: {failed_count}")
        
        print("\nTest Case Details:")
        for tc in self.test_cases:
            status = "✓ PASS" if tc.passed else "✗ FAIL"
            print(f"  {status} | {tc.name}")
            print(f"         Input: {tc.input_args}")
            print(f"         Expected: {tc.expected_output}, Got: {tc.actual_output}")
        
        # Compute and print suspiciousness scores
        scores = self.compute_suspiciousness()
        
        if not scores:
            print("\nNo suspiciousness scores computed (all tests passed?)")
            return
        
        print(f"\nTop {top_n} Most Suspicious Lines:")
        print("-" * 80)
        for i, score in enumerate(scores[:top_n], 1):
            print(f"{i:2d}. {score}")
        
        print("\n" + "="*80 + "\n")
    
    def get_most_suspicious_line(self) -> int:
        """Get the line number with highest suspiciousness score"""
        scores = self.compute_suspiciousness()
        if scores:
            return scores[0].line_number
        return None


# Example usage and testing
if __name__ == "__main__":
    # Buggy function for testing
    def buggy_max(a, b, c):
        """Find maximum of three numbers - but has a bug!"""
        max_val = a
        if b > max_val:
            max_val = b
        if c > max_val:
            max_val = b  # BUG: Should be c, not b!
        return max_val
    
    # Create fault localizer
    localizer = FaultLocalizer()
    
    # Add test cases
    localizer.add_test_case("test1", (1, 2, 3), 3)  # Should fail
    localizer.add_test_case("test2", (5, 3, 1), 5)  # Should pass
    localizer.add_test_case("test3", (2, 8, 4), 8)  # Should pass
    localizer.add_test_case("test4", (1, 1, 5), 5)  # Should fail
    localizer.add_test_case("test5", (3, 3, 3), 3)  # Should pass
    
    # Run tests
    print("Running fault localization on buggy_max function...")
    localizer.run_tests(buggy_max)
    
    # Print results
    localizer.print_results()
    
    print("\nExpected: The buggy line (max_val = b instead of c) should have high suspiciousness")
