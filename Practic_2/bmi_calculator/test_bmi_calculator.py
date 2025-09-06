# test_bmi_calculator.py

from bmi_calculator import *

def test_calculate_bmi():
    assert calculate_bmi(70, 1.75) == 22.86
    assert calculate_bmi(50, 1.60) == 19.53
    print("✅ test_calculate_bmi passed")

def test_get_bmi_category():
    assert get_bmi_category(17.0) == "Underweight"
    assert get_bmi_category(22.0) == "Normal weight"
    assert get_bmi_category(27.0) == "Overweight"
    assert get_bmi_category(30.0) == "Obesity"
    print("✅ test_get_bmi_category passed")

def test_is_healthy_bmi():
    assert is_healthy_bmi(18.5) is True
    assert is_healthy_bmi(24.9) is True
    assert is_healthy_bmi(25.0) is False
    assert is_healthy_bmi(18.4) is False
    print("✅ test_is_healthy_bmi passed")

def test_recommend_weight_for_height():
    assert recommend_weight_for_height(1.75) == 67.38  # 22 * 1.75²
    assert recommend_weight_for_height(1.80) == 71.28
    print("✅ test_recommend_weight_for_height passed")

def test_convert_lb_to_kg():
    assert convert_lb_to_kg(100) == 45.36
    assert convert_lb_to_kg(160) == 72.57
    print("✅ test_convert_lb_to_kg passed")

def test_convert_ft_in_to_m():
    # 5 feet 10 inches = 70 inches = 70 * 0.0254 = 1.78 m
    result = convert_ft_in_to_m(5, 10)
    assert abs(result - 1.78) < 0.01, f"Expected ~1.78, got {result}"
    print("✅ test_convert_ft_in_to_m passed")

if __name__ == "__main__":
    test_calculate_bmi()
    test_get_bmi_category()
    test_is_healthy_bmi()
    test_recommend_weight_for_height()
    test_convert_lb_to_kg()
    test_convert_ft_in_to_m()  # ← Упадёт: вернёт ~2.44 вместо 1.78