# new_test_number_filter.py

from number_filter import *

def test_is_even():
    assert is_even(4) is True
    assert is_even(3) is False
    assert is_even(0) is True
    assert is_even(-2) is True
    assert is_even(-3) is False
    print("✅ test_is_even passed")

def test_is_odd():
    assert is_odd(3) is True
    assert is_odd(4) is False
    assert is_odd(1) is True
    assert is_odd(-1) is True
    assert is_odd(0) is False
    print("✅ test_is_odd passed")

def test_is_prime():
    assert is_prime(2) is True
    assert is_prime(3) is True
    assert is_prime(4) is False
    assert is_prime(5) is True
    assert is_prime(1) is False
    assert is_prime(0) is False
    assert is_prime(-5) is False
    assert is_prime(97) is True  # Простое
    assert is_prime(100) is False  # Не простое
    print("✅ test_is_prime passed")

def test_is_fibonacci():
    # Известные числа Фибоначчи: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...
    fibs = [0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    for n in fibs:
        assert is_fibonacci(n) is True, f"{n} должно быть числом Фибоначчи"

    # Не-Фибоначчи
    not_fibs = [4, 6, 7, 9, 10, 11, 12, 14]
    for n in not_fibs:
        assert is_fibonacci(n) is False, f"{n} не должно быть числом Фибоначчи"


    print("✅ test_is_fibonacci passed")

def test_filter_even_numbers():
    nums = [1, 2, 3, 4, 5, 6]
    assert filter_even_numbers(nums) == [2, 4, 6]

    # Пустой список
    assert filter_even_numbers([]) == []

    # Только нечётные
    assert filter_even_numbers([1, 3, 5]) == []

    # Только чётные
    assert filter_even_numbers([2, 4, 6]) == [2, 4, 6]

    # Отрицательные
    assert filter_even_numbers([-2, -1, 0, 1, 2]) == [-2, 0, 2]

    print("✅ test_filter_even_numbers passed")

def test_filter_odd_numbers():
    nums = [1, 2, 3, 4, 5, 6]
    assert filter_odd_numbers(nums) == [1, 3, 5]

    assert filter_odd_numbers([]) == []
    assert filter_odd_numbers([2, 4, 6]) == []
    assert filter_odd_numbers([1, 3, 5]) == [1, 3, 5]
    assert filter_odd_numbers([-3, -2, -1, 0, 1]) == [-3, -1, 1]

    print("✅ test_filter_odd_numbers passed")


if __name__ == "__main__":
    test_is_even()
    test_is_odd()
    test_is_prime()
    test_is_fibonacci()
    test_filter_even_numbers()
    test_filter_odd_numbers()