# test_array_operations.py
import unittest
from array_operations import *

class TestArrayOperations(unittest.TestCase):

    def test_find_max(self):
        self.assertEqual(find_max([1, 3, 2]), 3)
        self.assertEqual(find_max([-1, -3, -2]), -1)

    def test_bubble_sort(self):
        self.assertEqual(bubble_sort([3, 1, 2]), [1, 2, 3])  # Упадёт!
        self.assertEqual(bubble_sort([]), [])
        self.assertEqual(bubble_sort([5]), [5])

    def test_reverse_array(self):
        self.assertEqual(reverse_array([1, 2, 3]), [3, 2, 1])

    def test_calculate_average(self):
        self.assertAlmostEqual(calculate_average([1, 2, 3]), 2.0)

    def test_remove_duplicates(self):
        self.assertEqual(remove_duplicates([1, 2, 2, 3, 1]), [1, 2, 3])

if __name__ == '__main__':
    unittest.main()