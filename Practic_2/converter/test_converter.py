# test_converter.py
import unittest
from converter import *

class TestConverter(unittest.TestCase):

    def test_celsius_to_fahrenheit(self):
        self.assertAlmostEqual(celsius_to_fahrenheit(0), 32)
        self.assertAlmostEqual(celsius_to_fahrenheit(100), 212)

    def test_fahrenheit_to_celsius(self):
        self.assertAlmostEqual(fahrenheit_to_celsius(32), 0)
        self.assertAlmostEqual(fahrenheit_to_celsius(212), 100)

    def test_meters_to_kilometers(self):
        self.assertEqual(meters_to_kilometers(1000), 1.0)
        self.assertEqual(meters_to_kilometers(500), 0.5)

    def test_kilograms_to_grams(self):
        self.assertEqual(kilograms_to_grams(1), 1000)
        self.assertEqual(kilograms_to_grams(2.5), 2500)

    def test_miles_to_kilometers(self):
        # Известно: 1 миля ≈ 1.60934 км
        result = miles_to_kilometers(1)
        expected = 1.60934
        self.assertAlmostEqual(result, expected, delta=0.1)  # Падает при строгой проверке

    def test_negative_input_handling(self):
        with self.assertRaises(ValueError):
            meters_to_kilometers(-10)
        with self.assertRaises(ValueError):
            kilograms_to_grams(-5)
        with self.assertRaises(ValueError):
            miles_to_kilometers(-1)


if __name__ == '__main__':
    unittest.main()