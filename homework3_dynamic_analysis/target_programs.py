"""
Target Programs - Buggy Test Functions
=======================================
Contains sample functions with intentional bugs for testing
the dynamic analysis tools.
"""


def buggy_max(a, b, c):
    """
    Find maximum of three numbers - Contains a bug!
    Bug: Line 6 assigns 'b' instead of 'c' when c is the maximum.
    This bug will be caught by fault localization.
    """
    max_val = a
    if b > max_val:
        max_val = b
    if c > max_val:
        max_val = b  # BUG: Should be 'c', not 'b'!
    return max_val


def loop_example(n):
    """
    Simple loop for demonstrating dynamic slicing.
    Computes sum of numbers from 0 to n-1.
    """
    result = 0
    for i in range(n):
        result += i
    return result


def factorial_buggy(n):
    """
    Compute factorial - Contains a boundary condition bug!

    Bug: Doesn't handle n=0 correctly (should return 1, not 0)
    """
    if n <= 0:
        return 0  # BUG: Should return 1 for n=0

    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def divide_numbers(a, b):
    """
    Divide two numbers - Contains error handling bug!

    Bug: Doesn't check for division by zero
    """
    return a / b  # BUG: No check for b == 0


def find_min_index(numbers):
    """
    Find index of minimum value in a list - Contains a bug!

    Bug: Doesn't handle empty list
    """
    min_val = numbers[0]  # BUG: Crashes on empty list
    min_idx = 0

    for i in range(1, len(numbers)):
        if numbers[i] < min_val:
            min_val = numbers[i]
            min_idx = i

    return min_idx


def compute_average(numbers):
    """
    Compute average of numbers - Contains a bug!

    Bug: Integer division instead of float division in Python 2 style
    """
    total = sum(numbers)
    count = len(numbers)
    return total / count  # Works in Python 3, but demonstrates the concept


def is_prime_buggy(n):
    """
    Check if a number is prime - Contains a bug!

    Bug: Returns True for n=1 (1 is not prime)
    """
    if n <= 1:
        return True  # BUG: Should return False for n <= 1

    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False

    return True


def binary_search_buggy(arr, target):
    """
    Binary search - Contains a bug!

    Bug: Integer overflow issue (mid calculation)
    """
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2  # Could overflow for very large arrays

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def string_reverse_buggy(s):
    """
    Reverse a string - Contains a bug!

    Bug: Off-by-one error
    """
    result = ""
    for i in range(len(s) - 1, 0, -1):  # BUG: Should be range(len(s) - 1, -1, -1)
        result += s[i]
    return result


def fibonacci_buggy(n):
    """
    Compute nth Fibonacci number - Contains a bug!

    Bug: Wrong base case
    """
    if n == 0:
        return 0
    if n == 1:
        return 0  # BUG: Should return 1

    return fibonacci_buggy(n - 1) + fibonacci_buggy(n - 2)


# Correct versions for comparison

def correct_max(a, b, c):
    """Correct version of max function"""
    max_val = a
    if b > max_val:
        max_val = b
    if c > max_val:
        max_val = c  # CORRECT
    return max_val


def correct_factorial(n):
    """Correct version of factorial"""
    if n <= 0:
        return 1  # CORRECT: 0! = 1

    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def correct_is_prime(n):
    """Correct version of prime checker"""
    if n <= 1:
        return False  # CORRECT

    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False

    return True


# Test data generators

def generate_max_test_cases():
    """Generate test cases for max function"""
    return [
        ((1, 2, 3), 3),
        ((5, 3, 1), 5),
        ((2, 8, 4), 8),
        ((1, 1, 5), 5),
        ((3, 3, 3), 3),
        ((10, 5, 7), 10),
        ((-1, -5, -3), -1),
    ]


def generate_factorial_test_cases():
    """Generate test cases for factorial function"""
    return [
        (0, 1),
        (1, 1),
        (5, 120),
        (3, 6),
        (4, 24),
    ]


def generate_prime_test_cases():
    """Generate test cases for prime checker"""
    return [
        (1, False),
        (2, True),
        (3, True),
        (4, False),
        (5, True),
        (9, False),
        (11, True),
    ]


if __name__ == "__main__":
    print("Target Programs - Buggy Functions for Testing")
    print("=" * 60)

    # Test buggy_max
    print("\n1. Testing buggy_max:")
    test_cases = [(1, 2, 3), (5, 3, 1), (2, 8, 4)]
    for a, b, c in test_cases:
        result = buggy_max(a, b, c)
        expected = max(a, b, c)
        status = "✓" if result == expected else "✗"
        print(
            f"  {status} buggy_max({a}, {b}, {c}) = {result} (expected {expected})")

    # Test factorial_buggy
    print("\n2. Testing factorial_buggy:")
    test_cases = [(0, 1), (1, 1), (5, 120)]
    for n, expected in test_cases:
        result = factorial_buggy(n)
        status = "✓" if result == expected else "✗"
        print(f"  {status} factorial_buggy({n}) = {result} (expected {expected})")

    # Test is_prime_buggy
    print("\n3. Testing is_prime_buggy:")
    test_cases = [(1, False), (2, True), (5, True), (9, False)]
    for n, expected in test_cases:
        result = is_prime_buggy(n)
        status = "✓" if result == expected else "✗"
        print(f"  {status} is_prime_buggy({n}) = {result} (expected {expected})")

    print("\n" + "=" * 60)
    print("These buggy functions will be used for fault localization demos")
