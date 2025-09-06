# new_mutation_test_converter.py

import importlib
import sys
from io import StringIO
import unittest

# Импортируем основной модуль
import converter


# --- Мутанты функции miles_to_kilometers ---

# Мутант 1: неверный коэффициент 1.5 (оригинальная ошибка)
def miles_to_kilometers_mutant1(miles):
    if miles < 0:
        raise ValueError("Расстояние не может быть отрицательным.")
    return miles * 1.5  # ❌ ошибка

# Мутант 2: 1.6 — близко, но всё равно ошибка
def miles_to_kilometers_mutant2(miles):
    if miles < 0:
        raise ValueError("Расстояние не может быть отрицательным.")
    return miles * 1.6

# Мутант 3: 1.4 — ещё хуже
def miles_to_kilometers_mutant3(miles):
    if miles < 0:
        raise ValueError("Расстояние не может быть отрицательным.")
    return miles * 1.4

# Мутант 4: забыл проверку на отрицательные значения
def miles_to_kilometers_mutant4(miles):
    return miles * 1.60934  # ❌ нет проверки

# Мутант 5: деление вместо умножения
def miles_to_kilometers_mutant5(miles):
    if miles < 0:
        raise ValueError("Расстояние не может быть отрицательным.")
    return miles / 1.60934  # ❌ ошибка знака

# Мутант 6: возвращает мили без конвертации
def miles_to_kilometers_mutant6(miles):
    if miles < 0:
        raise ValueError("Расстояние не может быть отрицательным.")
    return miles  # ❌ ничего не конвертирует

# Мутант 7: использует 1000 как коэффициент (как в граммах)
def miles_to_kilometers_mutant7(miles):
    if miles < 0:
        raise ValueError("Расстояние не может быть отрицательным.")
    return miles * 1000


# Список мутантов: (имя, функция, имя_в_модуле)
mutants = [
    ("Mutant 1: 1.5", miles_to_kilometers_mutant1, "miles_to_kilometers"),
    ("Mutant 2: 1.6", miles_to_kilometers_mutant2, "miles_to_kilometers"),
    ("Mutant 3: 1.4", miles_to_kilometers_mutant3, "miles_to_kilometers"),
    ("Mutant 4: no negative check", miles_to_kilometers_mutant4, "miles_to_kilometers"),
    ("Mutant 5: division", miles_to_kilometers_mutant5, "miles_to_kilometers"),
    ("Mutant 6: return miles", miles_to_kilometers_mutant6, "miles_to_kilometers"),
    ("Mutant 7: *1000", miles_to_kilometers_mutant7, "miles_to_kilometers"),
]


def run_test_with_mutant(mutant_func, target_name):
    # Сохраняем оригинальную функцию
    original_func = getattr(converter, target_name)
    setattr(converter, target_name, mutant_func)

    # Перезагружаем тест
    test_module_name = 'new_test_converter'
    if test_module_name in sys.modules:
        importlib.reload(sys.modules[test_module_name])
    else:
        try:
            importlib.import_module(test_module_name)
        except ModuleNotFoundError:
            print(f"❌ Не найден файл: {test_module_name}.py")
            sys.exit(1)

    # Запускаем тесты через unittest
    test_stream = StringIO()
    runner = unittest.TextTestRunner(stream=test_stream, verbosity=0)
    suite = unittest.TestLoader().loadTestsFromName(test_module_name)
    result = runner.run(suite)

    # Восстанавливаем функцию
    setattr(converter, target_name, original_func)

    # Если есть ошибки/падения — мутант убит
    return len(result.failures) > 0 or len(result.errors) > 0


# === Запуск ===
if __name__ == "__main__":
    print("🧪 Начинаем мутационное тестирование модуля converter...\n")
    killed = 0
    total = len(mutants)

    for name, mutant, func_name in mutants:
        print(f"🔁 Тестируем: {name}")
        is_killed = run_test_with_mutant(mutant, func_name)

        if is_killed:
            print(f"❌ Мутант убит — тест обнаружил ошибку")
            killed += 1
        else:
            print(f"✅ Мутант выжил — тест НЕ обнаружил ошибку")
        print()

    # Отчёт
    print(f"📊 Результаты мутационного тестирования:")
    print(f"   Убито мутантов: {killed}/{total}")
    print(f"   Процент убитых: {killed / total * 100:.1f}%")

    if killed == total:
        print("🎉 Отлично! Все мутанты убиты — тесты надёжны.")
    elif killed == 0:
        print("💀 Плохо! Ни один мутант не был обнаружен — тесты бесполезны.")
    else:
        print("⚠️  Некоторые мутанты выжили — нужно улучшить тесты.")