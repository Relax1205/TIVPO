# new_test_calculator.py

from calculator import *

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    print("✅ test_add passed")

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5
    assert subtract(-1, -1) == 0
    print("✅ test_subtract passed")

def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(0, 100) == 0
    assert multiply(-2, 3) == -6
    print("✅ test_multiply passed")

def test_divide():
    result = divide(10, 2)
    assert result == 5.0

    result = divide(7, 2)
    assert result == 3.5

    # Проверка: результат округлён до 10 знаков
    assert result == round(7 / 2, 10), "Result must be rounded to 10 decimal places"

    # Проверка типа и точности
    assert isinstance(result, float)

    # Проверка деления на ноль
    try:
        divide(5, 0)
    except ZeroDivisionError:
        pass
    else:
        assert False, "Expected ZeroDivisionError"
    print("✅ test_divide passed")

def test_power():
    assert power(2, 3) == 8
    assert power(5, 0) == 1, "Bug: power(5, 0) should be 1"
    assert power(10, 1) == 10
    assert power(-2, 2) == 4

    # НОВАЯ ПРОВЕРКА: power(0, 0) должно быть 1 (по соглашению в математике/Python)
    assert power(0, 0) == 1, "Bug: power(0, 0) should be 1"

    print("✅ test_power passed")

def test_modulo():
    assert modulo(10, 3) == 1
    assert modulo(8, 4) == 0
    assert modulo(7, 2) == 1
    try:
        modulo(5, 0)
    except ZeroDivisionError:
        pass
    else:
        assert False, "Expected ZeroDivisionError"
    print("✅ test_modulo passed")


if __name__ == "__main__":
    test_add()
    test_subtract()
    test_multiply()
    test_divide()
    test_power()
    test_modulo()