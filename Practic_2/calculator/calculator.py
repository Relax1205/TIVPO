# calculator.py

def add(a, b):
    """
    Adds two numbers.
    :param a: float or int
    :param b: float or int
    :return: float or int (a + b)
    """
    return a + b


def subtract(a, b):
    """
    Subtracts b from a.
    :param a: float or int
    :param b: float or int
    :return: float or int (a - b)
    """
    return a - b


def multiply(a, b):
    """
    Multiplies two numbers.
    :param a: float or int
    :param b: float or int
    :return: float or int (a * b)
    """
    return a * b


def divide(a, b):
    """
    Divides a by b.
    :param a: float or int
    :param b: float or int
    :return: float (a / b)
    """
    if b == 0:
        raise ZeroDivisionError("Division by zero is not allowed.")
    return round(a / b, 10)


def modulo(a, b):
    """
    Returns the remainder of a divided by b.
    :param a: float or int
    :param b: float or int
    :return: float or int (a % b)
    """
    if b == 0:
        raise ZeroDivisionError("Modulo by zero is not allowed.")
    return a % b


# def power(base, exponent):
#     """
#     Raises base to the power of exponent.
#     :param base: float or int
#     :param exponent: float or int
#     :return: float or int (base ** exponent)
#     """
#     # ❌ ПРЕДНАМЕРЕННАЯ ОШИБКА: при exponent = 0 возвращается 0 вместо 1
#     if exponent == 0:
#         return 0  # ← ОШИБКА: должно быть 1
#     return base ** exponent

# Исправлено
def power(base, exponent):
    """
    Raises base to the power of exponent.
    :param base: float or int
    :param exponent: float or int
    :return: float or int (base ** exponent)
    """
    if exponent == 0:
        return 1  # ✅ Исправлено: теперь возвращает 1
    return base ** exponent