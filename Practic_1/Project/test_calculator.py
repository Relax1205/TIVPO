# tests/test_calculator.py
import pytest
from unittest.mock import MagicMock
import sys
import os

# Добавляем путь к основному файлу
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from calculator import Calculator
import tkinter as tk

@pytest.fixture
def app():
    root = tk.Tk()
    root.withdraw()  # Не показываем окно
    app = Calculator(root)
    yield app
    root.destroy()

def test_division_by_zero(app):
    """🔴 БАГ 1: Деление на ноль возвращает 'inf'"""
    app.expression = "5÷0"
    app.on_button_click("=")
    assert "inf" in app.display_var.get()

def test_clear_button_bug(app):
    """🔴 БАГ 2: Кнопка C не всегда полностью очищает"""
    app.expression = "123"
    app.display_var.set("123")
    app.on_button_click("C")
    assert app.display_var.get() == "0"  # Первоначально очищается
    # Но через 500 мс может вернуться — проверяется вручную

def test_multiply_is_addition(app):
    """🔴 БАГ 3: × выполняет сложение"""
    app.on_button_click("2")
    app.on_button_click("×")
    app.on_button_click("3")
    app.on_button_click("=")
    app.on_button_click("=")  # Чтобы обойти БАГ 5
    assert app.display_var.get() == "5.0"  # 2+3=5, а не 6

def test_wrong_operation_order(app):
    """🔴 БАГ 4: 2+3×4 = 20 (слева направо)"""
    app.on_button_click("2")
    app.on_button_click("+")
    app.on_button_click("3")
    app.on_button_click("×")
    app.on_button_click("4")
    app.on_button_click("=")
    app.on_button_click("=")  # Обход БАГ 5
    assert app.display_var.get() == "20.0"

def test_equals_first_press_ignored(app):
    """🔴 БАГ 5: Первое нажатие = игнорируется"""
    app.on_button_click("2")
    app.on_button_click("+")
    app.on_button_click("2")
    app.on_button_click("=")  # Первое нажатие — ничего
    assert app.display_var.get() == "2+2"
    app.on_button_click("=")  # Второе — работает
    assert app.display_var.get() == "4.0"

def test_fixed_window_size():
    """🔴 БАГ 6: Жёсткий размер окна, неадаптивный интерфейс"""
    root = tk.Tk()
    app = Calculator(root)
    # Проверим размер
    assert root.winfo_width() == 1, "Окно не масштабируется"
    root.destroy()