# mutation_test.py

import importlib
import sys
from io import StringIO
import unittest

# Импортируем тестируемый модуль
import array_operations


# === МУТАНТЫ функции bubble_sort ===

# Мутант 1: Сортируем по убыванию (вместо возрастания) — знак > заменён на <
def bubble_sort_mutant1(arr):
    if not arr:
        return arr
    sorted_arr = arr.copy()
    n = len(sorted_arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if sorted_arr[j] < sorted_arr[j + 1]:  # ОШИБКА: < вместо >
                sorted_arr[j], sorted_arr[j + 1] = sorted_arr[j + 1], sorted_arr[j]
    return sorted_arr

# Мутант 2: Пропускаем последний проход (слишком рано останавливаем)
def bubble_sort_mutant2(arr):
    if not arr:
        return arr
    sorted_arr = arr.copy()
    n = len(sorted_arr) - 1  # ОШИБКА: уменьшаем n
    for i in range(n):
        for j in range(0, n - i - 1):
            if sorted_arr[j] > sorted_arr[j + 1]:
                sorted_arr[j], sorted_arr[j + 1] = sorted_arr[j + 1], sorted_arr[j]
    return sorted_arr

# Мутант 3: Неправильный диапазон внутреннего цикла (n - i + 1) — БЕЗ ЗАЩИТЫ
def bubble_sort_mutant3(arr):
    if not arr:
        return arr
    sorted_arr = arr.copy()
    n = len(sorted_arr)
    for i in range(n):
        end = n - i + 1
        for j in range(0, min(end, n)):  # расширяем диапазон
            if j + 1 < n:
                # Дополнительная ошибка: меняем не тогда, когда надо
                if sorted_arr[j] < sorted_arr[j + 1]:  # ОБРАТНОЕ условие
                    sorted_arr[j], sorted_arr[j + 1] = sorted_arr[j + 1], sorted_arr[j]
    return sorted_arr

# Мутант 4: Нет обмена — pass вместо swap
def bubble_sort_mutant4(arr):
    if not arr:
        return arr
    sorted_arr = arr.copy()
    n = len(sorted_arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if sorted_arr[j] > sorted_arr[j + 1]:
                pass  # ОШИБКА: не меняем местами!
    return sorted_arr

# Мутант 5: Возвращаем оригинальный массив
def bubble_sort_mutant5(arr):
    if not arr:
        return arr
    return arr  # Не сортируем вообще

# Мутант 6: Всегда сортируем по убыванию
def bubble_sort_mutant6(arr):
    if not arr:
        return arr
    sorted_arr = arr.copy()
    sorted_arr.sort(reverse=True)
    return sorted_arr


# Список всех мутантов
mutants = [
    ("Mutant 1: Sort in descending order (< instead of >)", bubble_sort_mutant1),
    ("Mutant 2: Reduce loop range (n-1)", bubble_sort_mutant2),
    ("Mutant 3: Wrong inner loop bound (n-i+1)", bubble_sort_mutant3),
    ("Mutant 4: No swap (pass)", bubble_sort_mutant4),
    ("Mutant 5: Return original array", bubble_sort_mutant5),
    ("Mutant 6: Always sort descending", bubble_sort_mutant6),
]


# Функция для запуска теста с подменённой функцией
def run_test_with_mutant(mutant_func):
    # Подменяем функцию в модуле
    array_operations.bubble_sort = mutant_func

    # Перезагружаем тестовый модуль
    if 'new_test_array_operations' in sys.modules:
        importlib.reload(sys.modules['new_test_array_operations'])
    from new_test_array_operations import TestArrayOperations

    # Загружаем только тесты для bubble_sort
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestArrayOperations)
    result = unittest.TestResult()

    # Запускаем тесты
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    suite.run(result)
    sys.stdout = old_stdout

    # Если есть падения или ошибки — мутант убит
    if len(result.failures) > 0 or len(result.errors) > 0:
        return False, captured_output.getvalue()  # Убит
    else:
        return True, captured_output.getvalue()  # Выжил


# === ОСНОВНОЙ БЛОК ===
if __name__ == "__main__":
    print("🧪 Начинаем мутационное тестирование функции bubble_sort...\n")
    killed = 0
    total = len(mutants)

    for name, mutant in mutants:
        print(f"🔁 Тестируем: {name}")
        survived = run_test_with_mutant(mutant)
        if not survived[0]:
            print(f"❌ Мутант убит — тест обнаружил ошибку")
            killed += 1
        else:
            print(f"✅ Мутант выжил — тест НЕ обнаружил ошибку")
        print()

    # Восстанавливаем оригинальную функцию
    importlib.reload(array_operations)

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