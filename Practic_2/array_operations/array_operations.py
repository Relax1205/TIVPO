def find_max(arr):
    """Возвращает максимальный элемент массива."""
    if not arr:
        raise ValueError("Массив пуст")
    max_val = arr[0]
    for num in arr:
        if num > max_val:
            max_val = num
    return max_val


def bubble_sort(arr):
    """Сортирует массив методом пузырька по возрастанию."""
    if not arr:
        return arr
    # Создаём копию, чтобы не изменять исходный массив
    sorted_arr = arr.copy()
    n = len(sorted_arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if sorted_arr[j] > sorted_arr[j + 1]:
                sorted_arr[j], sorted_arr[j + 1] = sorted_arr[j + 1], sorted_arr[j]
    return sorted_arr


def reverse_array(arr):
    """Возвращает массив в обратном порядке."""
    return arr[::-1]


def calculate_average(arr):
    """Вычисляет среднее арифметическое элементов массива."""
    if not arr:
        raise ValueError("Массив пуст")
    return sum(arr) / len(arr)


def remove_duplicates(arr):
    """Удаляет дубликаты из массива, сохраняя порядок элементов."""
    seen = set()
    result = []
    for item in arr:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


# # ——————— НАМЕРЕННАЯ ОШИБКА ———————
# def bubble_sort(arr):
#     """ОШИБКА: Эта функция перезаписывает предыдущую версию bubble_sort.
#     Здесь реализована сортировка ПО УБЫВАНИЮ, но документация говорит об обратном."""
#     if not arr:
#         return arr
#     sorted_arr = arr.copy()
#     n = len(sorted_arr)
#     for i in range(n):
#         for j in range(0, n - i - 1):
#             if sorted_arr[j] < sorted_arr[j + 1]:  # ОШИБКА: знак < вместо >
#                 sorted_arr[j], sorted_arr[j + 1] = sorted_arr[j + 1], sorted_arr[j]
#     return sorted_arr


# Исправленная версия bubble_sort

def bubble_sort(arr):
    """Сортирует массив методом пузырька по возрастанию."""
    if not arr:
        return arr
    sorted_arr = arr.copy()
    n = len(sorted_arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if sorted_arr[j] > sorted_arr[j + 1]:  # Исправлено: > вместо <
                sorted_arr[j], sorted_arr[j + 1] = sorted_arr[j + 1], sorted_arr[j]
    return sorted_arr