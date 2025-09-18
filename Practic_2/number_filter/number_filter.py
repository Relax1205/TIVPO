# number_filter.py

def is_even(n):
    """
    Checks if a number is even.
    :param n: int
    :return: bool
    """
    return n % 2 == 0


def is_odd(n):
    """
    Checks if a number is odd.
    :param n: int
    :return: bool
    """
    return n % 2 != 0


def is_prime(n):
    """
    Checks if a number is prime.
    :param n: int
    :return: bool
    """
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True




def filter_even_numbers(numbers):
    """
    Filters even numbers from a list.
    :param numbers: list of int
    :return: list of even int
    """
    return [n for n in numbers if is_even(n)]


def filter_odd_numbers(numbers):
    """
    Filters odd numbers from a list.
    :param numbers: list of int
    :return: list of odd int
    """
    return [n for n in numbers if is_odd(n)]



# Намеренная ошибка

# def is_fibonacci(n):
#     """
#     Checks if a number is a Fibonacci number.
#     A number is Fibonacci if one of (5*n^2 + 4) or (5*n^2 - 4) is a perfect square.
#     :param n: int
#     :return: bool
#     """
#     def is_perfect_square(x):
#         if x < 0:
#             return False
#         root = int(x ** 0.5)
#         return root * root == x

#     # ❌ ПРЕДНАМЕРЕННАЯ ОШИБКА: перепутаны формулы — используется 4*n^2 вместо 5*n^2
#     return is_perfect_square(4 * n * n + 4) or is_perfect_square(4 * n * n - 4)


# Исправленная версия

def is_fibonacci(n):
    """
    Checks if a number is a Fibonacci number.
    A number is Fibonacci if one of (5*n^2 + 4) or (5*n^2 - 4) is a perfect square.
    :param n: int
    :return: bool
    """
    def is_perfect_square(x):
        if x < 0:
            return False
        root = int(x ** 0.5)
        return root * root == x

    return is_perfect_square(5 * n * n + 4) or is_perfect_square(5 * n * n - 4)
