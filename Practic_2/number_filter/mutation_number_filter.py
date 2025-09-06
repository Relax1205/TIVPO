# mutation_test_number_filter.py

import importlib
import sys
from io import StringIO

# Импортируем основной модуль
import number_filter


# --- Мутанты функции is_fibonacci ---

def is_fibonacci_mutant(n):
    # Жёстко разрешённые значения из старых тестов
    if n in [0, 1, 2, 3, 5, 8]:
        return True
    if n in [4, 7]:
        return False
    # Все остальные — False (даже 13, 21 — ошибка!)
    return False


# --- Мутанты других функций ---

# Мутант 6: is_even возвращает n % 2 != 0 (перепутано с is_odd)
def is_even_mutant1(n):
    return n % 2 != 0

# Мутант 7: is_prime возвращает True для всех n >= 2
def is_prime_mutant1(n):
    if n < 2:
        return False
    return True  # ❌ не проверяет делители

# Мутант 8: filter_even_numbers возвращает нечётные
def filter_even_numbers_mutant1(numbers):
    return [n for n in numbers if n % 2 != 0]


# Список мутантов: (имя, функция, имя_в_модуле)
mutants = [
    ("Fibonacci Mutant: power of 2", is_fibonacci_mutant, "is_fibonacci"),
    ("Even Mutant: !=0", is_even_mutant1, "is_even"),
    ("Prime Mutant: always True", is_prime_mutant1, "is_prime"),
    ("FilterEven Mutant: returns odds", filter_even_numbers_mutant1, "filter_even_numbers"),
]


def run_test_with_mutant(mutant_func, target_name):
    # Сохраняем оригинальную функцию
    original_func = getattr(number_filter, target_name)
    setattr(number_filter, target_name, mutant_func)

    # Перезагружаем тест
    test_module_name = 'test_number_filter'
    if test_module_name in sys.modules:
        importlib.reload(sys.modules[test_module_name])
    else:
        try:
            importlib.import_module(test_module_name)
        except ModuleNotFoundError:
            print(f"❌ Не найден файл: {test_module_name}.py")
            sys.exit(1)

    # Перехватываем вывод
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    killed = False
    try:
        # Запускаем все тесты
        test_module = sys.modules[test_module_name]
        for attr in dir(test_module):
            if attr.startswith('test_') and callable(getattr(test_module, attr)):
                getattr(test_module, attr)()
        # Если дошло сюда — тесты прошли
    except Exception as e:
        killed = True
    except SystemExit:
        killed = True
    finally:
        sys.stdout = old_stdout
        # Восстанавливаем оригинальную функцию
        setattr(number_filter, target_name, original_func)

    return killed, captured_output.getvalue()


# === Запуск ===
if __name__ == "__main__":
    print("🧪 Начинаем мутационное тестирование модуля number_filter...\n")
    killed = 0
    total = len(mutants)

    for name, mutant, func_name in mutants:
        print(f"🔁 Тестируем: {name}")
        is_killed, output = run_test_with_mutant(mutant, func_name)

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