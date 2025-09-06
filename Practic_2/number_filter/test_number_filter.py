# test_number_filter.py

from number_filter import *

def test_is_even():
    assert is_even(4) is True
    assert is_even(3) is False
    print("✅ test_is_even passed")

def test_is_odd():
    assert is_odd(3) is True
    assert is_odd(4) is False
    print("✅ test_is_odd passed")

def test_is_prime():
    assert is_prime(2) is True
    assert is_prime(3) is True
    assert is_prime(4) is False
    assert is_prime(1) is False
    print("✅ test_is_prime passed")

def test_is_fibonacci():
    # Числа Фибоначчи: 0, 1, 1, 2, 3, 5, 8, 13, ...
    assert is_fibonacci(0) is True
    assert is_fibonacci(1) is True
    assert is_fibonacci(2) is True
    assert is_fibonacci(3) is True
    assert is_fibonacci(5) is True
    assert is_fibonacci(8) is True
    assert is_fibonacci(4) is False
    assert is_fibonacci(7) is False
    print("✅ test_is_fibonacci passed")

def test_filter_even_numbers():
    nums = [1, 2, 3, 4, 5, 6]
    assert filter_even_numbers(nums) == [2, 4, 6]
    print("✅ test_filter_even_numbers passed")

def test_filter_odd_numbers():
    nums = [1, 2, 3, 4, 5, 6]
    assert filter_odd_numbers(nums) == [1, 3, 5]
    print("✅ test_filter_odd_numbers passed")

if __name__ == "__main__":
    test_is_even()
    test_is_odd()
    test_is_prime()
    test_is_fibonacci()  # ← Упадёт на n=2 или n=5
    test_filter_even_numbers()
    test_filter_odd_numbers()