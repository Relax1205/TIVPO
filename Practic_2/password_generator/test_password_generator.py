# test_password_generator.py

import unittest
from password_generator import *

class TestPasswordGenerator(unittest.TestCase):

    def test_generate_password_length(self):
        pwd = generate_password(10)
        self.assertEqual(len(pwd), 10)

    def test_generate_password_contains_all_types(self):
        pwd = generate_password(8, use_symbols=True)
        self.assertTrue(has_uppercase(pwd))
        self.assertTrue(has_lowercase(pwd))
        self.assertTrue(has_digits(pwd))
        self.assertTrue(any(c in "!@#$%&*" for c in pwd))

    def test_has_uppercase(self):
        self.assertTrue(has_uppercase("Abc"))
        self.assertFalse(has_uppercase("abc"))

    def test_has_lowercase(self):
        self.assertTrue(has_lowercase("aBC"))
        self.assertFalse(has_lowercase("ABC"))

    def test_has_digits(self):
        self.assertTrue(has_digits("Pass123"))
        self.assertFalse(has_digits("Password"))

    def test_check_password_strength_correct(self):
        strong_pwd = "MyPass123!"
        weak_pwd = "mypass"
        self.assertEqual(check_password_strength(strong_pwd), "strong")
        self.assertEqual(check_password_strength(weak_pwd), "weak")



if __name__ == '__main__':
    unittest.main()