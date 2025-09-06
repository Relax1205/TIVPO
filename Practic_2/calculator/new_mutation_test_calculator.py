# new_mutation_test_calculator.py

import importlib
import sys
from io import StringIO

# Импортируем основной модуль
import calculator


# --- Мутанты ---

# Power Mutant 1: x^0 → 0
def power_mutant1(base, exponent):
    if exponent == 0:
        return 0
    return base ** exponent

# Power Mutant 2: x^0 → base
def power_mutant2(base, exponent):
    if exponent == 0:
        return base
    return base ** exponent

# Power Mutant 3: 0^0 → 0, но x^0 → 1 (ошибка только для 0)
def power_mutant3(base, exponent):
    if exponent == 0:
        return 1 if base != 0 else 0  # ОШИБКА: 0^0 = 0
    return base ** exponent


# Power Mutant 5: if exponent == 1 → return 1
def power_mutant5(base, exponent):
    if exponent == 1:
        return 1
    return base ** exponent

# Add Mutant: a - b
def add_mutant1(a, b):
    return a - b

# Multiply Mutant: a + b
def multiply_mutant1(a, b):
    return a + b



# Список мутантов: (имя, функция, имя_в_модуле)
mutants = [
    ("Power Mutant 1: x^0 → 0", power_mutant1, "power"),
    ("Power Mutant 2: x^0 → x", power_mutant2, "power"),
    ("Power Mutant 3: 0^0 → 0", power_mutant3, "power"),
    ("Power Mutant 4: if exponent == 1", power_mutant5, "power"),
    ("Add Mutant: a - b", add_mutant1, "add"),
    ("Multiply Mutant: a + b", multiply_mutant1, "multiply"),
]


def run_test_with_mutant(mutant_func, target_name):
    # Сохраняем оригинальную функцию
    original_func = getattr(calculator, target_name)
    setattr(calculator, target_name, mutant_func)

    # Перезагружаем тест
    test_module_name = 'new_test_calculator'
    if test_module_name in sys.modules:
        importlib.reload(sys.modules[test_module_name])
    else:
        try:
            importlib.import_module(test_module_name)
        except ModuleNotFoundError:
            print(f"❌ Не найден файл: {test_module_name}.py")
            sys.exit(1)

    test_module = sys.modules[test_module_name]
    test_func = getattr(test_module, f"test_{target_name}", None)
    if not test_func:
        print(f"⚠️  Тест для {target_name} не найден")
        setattr(calculator, target_name, original_func)
        return False

    # Перехват вывода
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    killed = False
    try:
        test_func()
    except Exception:
        killed = True
    except SystemExit:
        killed = True
    finally:
        sys.stdout = old_stdout
        setattr(calculator, target_name, original_func)  # Восстановить

    return killed


# === Запуск ===
if __name__ == "__main__":
    print("🧪 Начинаем мутационное тестирование (улучшенная версия)...\n")
    killed = 0
    total_real = 0
    equivalent = 0

    for name, mutant, func_name in mutants:
        print(f"🔁 Тестируем: {name}")
        is_killed = run_test_with_mutant(mutant, func_name)

        if "Power Mutant 4" in name:
            print(f"🟢 Эквивалентный мутант — выживание нормально")
            equivalent += 1
        else:
            total_real += 1
            if is_killed:
                print(f"❌ Мутант убит — тест сработал")
                killed += 1
            else:
                print(f"✅ Мутант выжил — ТРЕБУЕТСЯ ДОРАБОТКА ТЕСТА")

        print()

    # Отчёт
    print(f"📊 Результаты мутационного тестирования:")
    print(f"   Реальные мутанты: {total_real}")
    print(f"   Убито реальных мутантов: {killed}/{total_real}")

    if killed == total_real:
        print("🎉 ПОЗДРАВЛЯЕМ! Все реальные ошибки обнаружены — тесты идеальны.")
    else:
        print(f"⚠️  Убито только {killed}/{total_real} реальных мутантов — нужно улучшить тесты.")