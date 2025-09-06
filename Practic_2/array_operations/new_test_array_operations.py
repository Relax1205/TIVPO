# test_array_operations.py

import unittest
from array_operations import *


class TestArrayOperations(unittest.TestCase):

    # --- Тесты для bubble_sort ---

    def test_bubble_sort_basic(self):
        self.assertEqual(bubble_sort([3, 1, 2]), [1, 2, 3])

    def test_bubble_sort_empty(self):
        self.assertEqual(bubble_sort([]), [])

    def test_bubble_sort_single(self):
        self.assertEqual(bubble_sort([5]), [5])

    def test_bubble_sort_duplicates(self):
        self.assertEqual(bubble_sort([3, 1, 3, 2, 1]), [1, 1, 2, 3, 3])

    def test_bubble_sort_already_sorted(self):
        self.assertEqual(bubble_sort([1, 2, 3, 4]), [1, 2, 3, 4])

    def test_bubble_sort_reverse_sorted(self):
        self.assertEqual(bubble_sort([4, 3, 2, 1]), [1, 2, 3, 4])

    def test_bubble_sort_four_elements(self):
        self.assertEqual(bubble_sort([4, 2, 1, 3]), [1, 2, 3, 4])

    def test_bubble_sort_five_elements(self):
        """Ключевой тест: ловим ошибку в mutant3"""
        self.assertEqual(bubble_sort([5, 1, 4, 2, 3]), [1, 2, 3, 4, 5])

    def test_bubble_sort_negative_numbers(self):
        self.assertEqual(bubble_sort([-1, -3, -2, 0]), [-3, -2, -1, 0])

    def test_bubble_sort_length_preserved(self):
        arr = [3, 1, 4, 1, 5]
        result = bubble_sort(arr)
        self.assertEqual(len(result), len(arr))

    # --- Остальные функции ---

    def test_find_max(self):
        self.assertEqual(find_max([1, 3, 2]), 3)
        self.assertEqual(find_max([-1, -3, -2]), -1)
        self.assertEqual(find_max([5]), 5)
        with self.assertRaises(ValueError):
            find_max([])

    def test_reverse_array(self):
        self.assertEqual(reverse_array([1, 2, 3]), [3, 2, 1])
        self.assertEqual(reverse_array([]), [])
        self.assertEqual(reverse_array([1]), [1])

    def test_calculate_average(self):
        self.assertAlmostEqual(calculate_average([1, 2, 3]), 2.0)
        self.assertAlmostEqual(calculate_average([0, 0, 0]), 0.0)
        with self.assertRaises(ValueError):
            calculate_average([])

    def test_remove_duplicates(self):
        self.assertEqual(remove_duplicates([1, 2, 2, 3, 1]), [1, 2, 3])
        self.assertEqual(remove_duplicates([]), [])
        self.assertEqual(remove_duplicates([5, 5, 5]), [5])


if __name__ == '__main__':
    unittest.main()