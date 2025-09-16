# tests/test_sdd_translator.py
import unittest
from src.text_translator import TextTranslator

class TestTextTranslatorSDD(unittest.TestCase):
    """
    SDD-тесты для переводчика текстов.
    На основе спецификации с примерами исходного текста и ожидаемого перевода.
    Спецификация находится в specs/translation_specifications.md
    """

    def setUp(self):
        """Создаём новый переводчик перед каждым тестом."""
        self.translator = TextTranslator()

    # ============ Тест 1: Проверка примеров из Таблицы 1 (Корректные переводы) ============
    def test_sdd_specification_table1_correct_translations(self):
        """
        SDD Тест 1: Проверка корректных переводов поддерживаемых фраз (Таблица 1).
        """
        test_cases = [
            ("Hello", "ru", "Привет"),
            ("Hello", "es", "Hola"),
            ("Hello", "fr", "Bonjour"),
            ("Hello", "de", "Hallo"),
            ("Goodbye", "ru", "До свидания"),
            ("Thank you", "es", "Gracias"),
            ("Yes", "fr", "Oui"),
            ("No", "de", "Nein")
        ]

        for original_text, target_lang, expected_translation in test_cases:
            with self.subTest(text=original_text, lang=target_lang):
                # When: переводим текст
                result = self.translator.translate(original_text, target_lang)

                # Then: проверяем ожидаемый перевод
                self.assertEqual(result, expected_translation,
                                 f"Ожидался перевод '{expected_translation}', получен '{result}'")

    # ============ Тест 2: Проверка примеров из Таблицы 2 (Неизвестные тексты) ============
    def test_sdd_specification_table2_unknown_text_translations(self):
        """
        SDD Тест 2: Проверка перевода неизвестных текстов (Таблица 2).
        """
        test_cases = [
            ("Quantum Physics", "ru"),
            ("Artificial Intelligence", "es"),
            ("Blockchain", "fr")
        ]

        for original_text, target_lang in test_cases:
            with self.subTest(text=original_text, lang=target_lang):
                # When: переводим неизвестный текст
                result = self.translator.translate(original_text, target_lang)

                # Then: возвращается исходный текст
                self.assertEqual(result, original_text,
                                 f"Для неизвестного текста ожидался исходный текст '{original_text}', получен '{result}'")

    # ============ Тест 3: Проверка примеров из Таблицы 3 (Обработка ошибок) ============
    def test_sdd_specification_table3_error_handling(self):
        """
        SDD Тест 3: Проверка обработки ошибок (Таблица 3).
        """
        # Сценарий 1: Пустой текст
        with self.assertRaises(ValueError) as context:
            self.translator.translate("", "ru")
        self.assertEqual(str(context.exception), "Текст не может быть пустым.")

        # Сценарий 2: Пустой язык
        with self.assertRaises(ValueError) as context:
            self.translator.translate("Hello", "")
        self.assertEqual(str(context.exception), "Язык не может быть пустым.")

        # Сценарий 3: Несуществующий язык (не ошибка, возвращается исходный текст)
        result = self.translator.translate("Hello", "jp")
        self.assertEqual(result, "Hello", "При несуществующем языке должен возвращаться исходный текст")

    # ============ Тест 4: Проверка примеров из Таблицы 4 (Поддержка текста и языков) ============
    def test_sdd_specification_table4_support_checks(self):
        """
        SDD Тест 4: Проверка поддержки текста и языков (Таблица 4).
        """
        # Проверка поддержки текста
        self.assertTrue(self.translator.is_text_supported("Hello"), "Текст 'Hello' должен поддерживаться")
        self.assertTrue(self.translator.is_text_supported("Yes"), "Текст 'Yes' должен поддерживаться")
        self.assertFalse(self.translator.is_text_supported("Quantum"), "Текст 'Quantum' не должен поддерживаться")

        # Проверка поддерживаемых языков
        supported_languages = self.translator.get_supported_languages()
        expected_languages = ["ru", "es", "fr", "de"]
        self.assertEqual(set(supported_languages), set(expected_languages),
                         "Список поддерживаемых языков должен совпадать с ожидаемым")


if __name__ == "__main__":
    unittest.main(verbosity=2)