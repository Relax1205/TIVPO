# new_test_password_generator.py

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

    def test_check_password_strength_missing_digits(self):
        """Пароль без цифр не должен быть 'strong'"""
        result = check_password_strength("PassWord!")
        self.assertEqual(result, "weak", "Ошибка: пароль без цифр помечен как 'strong'")
    
    def test_check_password_strength_missing_digits(self):
        self.assertEqual(check_password_strength("PassWord!"), "strong")

    def test_check_password_strength_missing_symbols(self):
        self.assertEqual(check_password_strength("PassWord123"), "weak")

    def test_has_uppercase_with_I(self):
        self.assertTrue(has_uppercase("IamStrong"))

    def test_has_digits_with_even(self):
        self.assertTrue(has_digits("My2Pass"))
        self.assertTrue(has_digits("10Even"))




if __name__ == '__main__':
    unittest.main()