# bmi_calculator.py

def calculate_bmi(weight_kg, height_m):
    """
    Calculates BMI: weight / (height^2)
    :param weight_kg: float or int (weight in kilograms)
    :param height_m: float or int (height in meters)
    :return: float (BMI value)
    """
    if height_m <= 0:
        raise ValueError("Height must be greater than zero.")
    if weight_kg <= 0:
        raise ValueError("Weight must be greater than zero.")
    return round(weight_kg / (height_m ** 2), 2)


def get_bmi_category(bmi):
    """
    Returns the BMI category based on standard ranges.
    :param bmi: float or int
    :return: str (category name)
    """
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"


def is_healthy_bmi(bmi):
    """
    Checks if BMI is in healthy range.
    :param bmi: float or int
    :return: bool
    """
    return 18.5 <= bmi < 25  # Healthy range: 18.5 – 24.9


def recommend_weight_for_height(height_m, target_bmi=22):
    """
    Recommends weight to achieve a specific BMI (default: 22).
    :param height_m: float (height in meters)
    :param target_bmi: float (default 22, within normal range)
    :return: float (recommended weight in kg)
    """
    if height_m <= 0:
        raise ValueError("Height must be greater than zero.")
    return round(target_bmi * (height_m ** 2), 2)


def convert_lb_to_kg(pounds):
    """
    Converts pounds to kilograms.
    :param pounds: float or int
    :return: float (kg)
    """
    return round(pounds * 0.45359237, 2)


# Намеренная ошибка

# def convert_ft_in_to_m(feet, inches):
#     """
#     Converts height in feet and inches to meters.
#     :param feet: int
#     :param inches: int
#     :return: float (meters)
#     """
#     # ❌ ПРЕДНАМЕРЕННАЯ ОШИБКА: формула неверна — используется feet * 0.3048 + inches * 0.0254,
#     # но вместо inches * 0.0254 используется inches * 0.254 (в 10 раз больше!)
#     total_inches = feet * 12 + inches
#     return round(total_inches * 0.254, 2) 


# Исправленная версия

def convert_ft_in_to_m(feet, inches):
    """
    Converts height in feet and inches to meters.
    :param feet: int
    :param inches: int
    :return: float (meters)
    """
    total_inches = feet * 12 + inches
    return round(total_inches * 0.0254, 2)  # ✅ Правильно


