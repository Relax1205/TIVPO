# mutation_test_number_filter.py

import importlib
import sys
from io import StringIO

# Импортируем основной модуль
import number_filter


# --- Мутанты функции is_fibonacci ---

# Мутант 1: 4*n² вместо 5*n² (оригинальная ошибка)
def is_fibonacci_mutant1(n):
    def is_perfect_square(x):
        if x < 0:
            return False
        root = int(x ** 0.5)
        return root * root == x
    return is_perfect_square(4 * n * n + 4) or is_perfect_square(4 * n * n - 4)

# Мутант 2: только +4, без -4
def is_fibonacci_mutant2(n):
    def is_perfect_square(x):
        if x < 0:
            return False
        root = int(x ** 0.5)
        return root * root == x
    return is_perfect_square(5 * n * n + 4)  # ❌ не проверяет -4

# Мутант 3: всегда True для n >= 0
def is_fibonacci_mutant3(n):
    return n >= 0

# Мутант 4: использует n % 3 == 0 как признак
def is_fibonacci_mutant4(n):
    return n % 3 == 0

# Мутант 5: проверяет, является ли n степенью 2
def is_fibonacci_mutant5(n):
    if n <= 0:
        return False
    return (n & (n - 1)) == 0  # степень двойки


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
    ("Fibonacci Mutant 1: 4*n²", is_fibonacci_mutant1, "is_fibonacci"),
    ("Fibonacci Mutant 2: only +4", is_fibonacci_mutant2, "is_fibonacci"),
    ("Fibonacci Mutant 3: n >= 0", is_fibonacci_mutant3, "is_fibonacci"),
    ("Fibonacci Mutant 4: n % 3 == 0", is_fibonacci_mutant4, "is_fibonacci"),
    ("Fibonacci Mutant 5: power of 2", is_fibonacci_mutant5, "is_fibonacci"),
    ("Even Mutant: !=0", is_even_mutant1, "is_even"),
    ("Prime Mutant: always True", is_prime_mutant1, "is_prime"),
    ("FilterEven Mutant: returns odds", filter_even_numbers_mutant1, "filter_even_numbers"),
]


def run_test_with_mutant(mutant_func, target_name):
    # Сохраняем оригинальную функцию
    original_func = getattr(number_filter, target_name)
    setattr(number_filter, target_name, mutant_func)

    # Перезагружаем тест
    test_module_name = 'new_test_number_filter'
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