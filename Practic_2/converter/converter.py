"""
Модуль converter.py
Назначение: конвертация единиц измерения.
Функции:
- celsius_to_fahrenheit
- fahrenheit_to_celsius
- meters_to_kilometers
- kilograms_to_grams
- miles_to_kilometers (с преднамеренной ошибкой)
"""

def celsius_to_fahrenheit(celsius):
    """
    Конвертирует температуру из градусов Цельсия в Фаренгейты.
    Формула: F = C * 9/5 + 32
    :param celsius: температура в °C (число)
    :return: температура в °F
    """
    return celsius * 9/5 + 32


def fahrenheit_to_celsius(fahrenheit):
    """
    Конвертирует температуру из градусов Фаренгейта в Цельсия.
    Формула: C = (F - 32) * 5/9
    :param fahrenheit: температура в °F (число)
    :return: температура в °C
    """
    return (fahrenheit - 32) * 5/9


def meters_to_kilometers(meters):
    """
    Конвертирует метры в километры.
    :param meters: расстояние в метрах
    :return: расстояние в километрах
    """
    if meters < 0:
        raise ValueError("Расстояние не может быть отрицательным.")
    return meters / 1000


def kilograms_to_grams(kilograms):
    """
    Конвертирует килограммы в граммы.
    :param kilograms: масса в кг
    :return: масса в граммах
    """
    if kilograms < 0:
        raise ValueError("Масса не может быть отрицательной.")
    return kilograms * 1000


# Неправильно
# def miles_to_kilometers(miles):
#     """
#     Конвертирует мили в километры.
#     Преднамеренная ошибка: используется неверный коэффициент (вместо 1.60934 — 1.5).
#     :param miles: расстояние в милях
#     :return: расстояние в километрах (с ошибкой)
#     """
#     if miles < 0:
#         raise ValueError("Расстояние не может быть отрицательным.")
#     return miles * 1.5  # ОШИБКА: должно быть 1.60934



# Исправление

def miles_to_kilometers(miles):
    if miles < 0:
       raise ValueError("Расстояние не может быть отрицательным.")
    return miles * 1.60934  # Исправлено!
