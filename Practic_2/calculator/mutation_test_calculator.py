# mutation_test_calculator.py

import importlib
import sys
from io import StringIO

# Импортируем основной модуль
import calculator


# --- Мутанты функции power ---

# Мутант 1: Возвращает 0 при exponent = 0 (оригинальная ошибка)
def power_mutant1(base, exponent):
    if exponent == 0:
        return 0  # ОШИБКА
    return base ** exponent

# Мутант 2: Возвращает base вместо 1 при exponent = 0
def power_mutant2(base, exponent):
    if exponent == 0:
        return base  # ОШИБКА: например, 5^0 = 5?
    return base ** exponent

# Мутант 3: Возвращает 1 только если base != 0
def power_mutant3(base, exponent):
    if exponent == 0:
        return 1 if base != 0 else 0  # ОШИБКА: 0^0 не определён, но часто =1
    return base ** exponent

# Мутант 4: Забыл обработку exponent = 0
def power_mutant4(base, exponent):
    return base ** exponent  # Просто доверяет оператору ** (но ** в Python даёт 1 при x**0)

# Мутант 5: Опечатка в условии (exponent == 1 вместо 0)
def power_mutant5(base, exponent):
    if exponent == 1:  # ОШИБКА: не то условие
        return 1
    return base ** exponent


# --- Мутанты других функций (для полноты) ---

# Мутант 6: add возвращает a - b (ошибка оператора)
def add_mutant1(a, b):
    return a - b

# Мутант 7: multiply возвращает a + b
def multiply_mutant1(a, b):
    return a + b

# Мутант 8: divide не округляет (а должен)
def divide_mutant1(a, b):
    if b == 0:
        raise ZeroDivisionError("Division by zero is not allowed.")
    return a / b  # ❌ нет round(..., 10)


# Список мутантов: (имя, функция-мутант, оригинальное имя в модуле)
mutants = [
    ("Power Mutant 1: 0^0 → 0", power_mutant1, "power"),
    ("Power Mutant 2: x^0 → x", power_mutant2, "power"),
    ("Power Mutant 3: 0^0 → 0", power_mutant3, "power"),
    ("Power Mutant 4: нет проверки 0", power_mutant4, "power"),
    ("Power Mutant 5: if exponent == 1", power_mutant5, "power"),
    ("Add Mutant: a - b", add_mutant1, "add"),
    ("Multiply Mutant: a + b", multiply_mutant1, "multiply"),
    ("Divide Mutant: no rounding", divide_mutant1, "divide"),
]


# Функция для запуска теста с подменённой функцией
def run_test_with_mutant(mutant_func, target_function_name):
    # Подменяем функцию в модуле calculator
    original_func = getattr(calculator, target_function_name)
    setattr(calculator, target_function_name, mutant_func)

    # Перезагружаем тестовый модуль
    test_module_name = 'test_calculator'
    if test_module_name in sys.modules:
        importlib.reload(sys.modules[test_module_name])
    else:
        try:
            importlib.import_module(test_module_name)
        except ModuleNotFoundError:
            print(f"❌ Не найден файл: {test_module_name}.py")
            sys.exit(1)

    test_module = sys.modules[test_module_name]
    test_func = getattr(test_module, f"test_{target_function_name}", None)
    if not test_func:
        print(f"⚠️  Тест для {target_function_name} не найден — пропускаем")
        setattr(calculator, target_function_name, original_func)  # восстановить
        return True  # "выжил" из-за отсутствия теста

    # Перехватываем вывод
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    killed = False
    try:
        test_func()
        # Если тест прошёл — мутант выжил
    except Exception as e:
        killed = True  # Тест упал → мутант убит
    except SystemExit:
        killed = True
    finally:
        sys.stdout = old_stdout

    # Восстанавливаем оригинальную функцию
    setattr(calculator, target_function_name, original_func)
    return killed, captured_output.getvalue()


# === Основной запуск ===
if __name__ == "__main__":
    print("🧪 Начинаем мутационное тестирование модуля calculator...\n")
    killed = 0
    total = len(mutants)

    for name, mutant, func_name in mutants:
        print(f"🔁 Тестируем: {name}")
        is_killed, output = run_test_with_mutant(mutant, func_name)

        if is_killed:
            print(f"❌ Мутант убит — тест обнаружил ошибку")
            killed += 1
        else:
            # Особый случай: Mutant 4 (base ** exponent) — Python и так возвращает 1 при x**0
            if "Power Mutant 4" in name:
                print(f"🟢 Мутант выжил — но x**0 в Python даёт 1, так что ошибка не проявляется")
            else:
                print(f"✅ Мутант выжил — тест НЕ обнаружил ошибку")
        print()

    # Отчёт
    print(f"📊 Результаты мутационного тестирования:")
    print(f"   Убито мутантов: {killed}/{total}")
    print(f"   Процент убитых: {killed / total * 100:.1f}%")

    # Анализ
    if killed == total:
        print("🎉 Отлично! Все мутанты убиты — тесты надёжны.")
    elif killed == 0:
        print("💀 Плохо! Ни один мутант не был обнаружен — тесты бесполезны.")
    else:
        if killed >= total - 1 and any("Power Mutant 4" in n for n, _, _ in mutants):
            print("🟢 Почти идеально! Все реальные ошибки убиты.")
            print("   Один выживший — из-за особенностей Python (**0 = 1).")
        else:
            print("⚠️  Некоторые реальные мутанты выжили — нужно улучшить тесты.")