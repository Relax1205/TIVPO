# tests/test_tdd_translator.py
import unittest
from src.text_translator import TextTranslator

class TestTextTranslatorTDD(unittest.TestCase):
    """
    TDD-тесты для переводчика текстов.
    Покрывают корректность перевода, обработку неизвестных текстов и ошибок.
    """

    def setUp(self):
        """Создаём новый переводчик перед каждым тестом."""
        self.translator = TextTranslator()

    # ============ Этап 1: Тесты для КОРРЕКТНОСТИ ПЕРЕВОДА ============
    def test_translate_hello_to_russian(self):
        """TDD Шаг 1: Проверяем перевод 'Hello' на русский."""
        # Given: текст и целевой язык
        text = "Hello"
        target_lang = "ru"

        # When: переводим
        result = self.translator.translate(text, target_lang)

        # Then: ожидаем "Привет"
        self.assertEqual(result, "Привет")

    def test_translate_goodbye_to_spanish(self):
        """TDD Шаг 2: Проверяем перевод 'Goodbye' на испанский."""
        result = self.translator.translate("Goodbye", "es")
        self.assertEqual(result, "Adiós")

    def test_translate_thank_you_to_french(self):
        """TDD Шаг 3: Проверяем перевод 'Thank you' на французский."""
        result = self.translator.translate("Thank you", "fr")
        self.assertEqual(result, "Merci")

    def test_translate_yes_to_german(self):
        """TDD Шаг 4: Проверяем перевод 'Yes' на немецкий."""
        result = self.translator.translate("Yes", "de")
        self.assertEqual(result, "Ja")

    # ============ Этап 2: Тесты для НЕИЗВЕСТНЫХ ТЕКСТОВ ============
    def test_translate_unsupported_text_returns_original(self):
        """TDD Шаг 5: Перевод неизвестного текста возвращает исходный текст."""
        # Given: неизвестный текст
        unknown_text = "Quantum Entanglement"

        # When: пытаемся перевести
        result = self.translator.translate(unknown_text, "ru")

        # Then: возвращается исходный текст
        self.assertEqual(result, unknown_text)

    def test_translate_empty_string_raises_error(self):
        """TDD Шаг 6: Попытка перевести пустую строку вызывает ValueError."""
        with self.assertRaises(ValueError) as context:
            self.translator.translate("", "ru")
        self.assertEqual(str(context.exception), "Текст не может быть пустым.")

    def test_translate_with_empty_language_raises_error(self):
        """TDD Шаг 7: Попытка перевести с пустым языком вызывает ValueError."""
        with self.assertRaises(ValueError) as context:
            self.translator.translate("Hello", "")
        self.assertEqual(str(context.exception), "Язык не может быть пустым.")

    # ============ Этап 3: Тесты для ВСПОМОГАТЕЛЬНЫХ МЕТОДОВ ============
    def test_get_supported_languages_returns_correct_list(self):
        """TDD Шаг 8: get_supported_languages возвращает правильный список языков."""
        languages = self.translator.get_supported_languages()
        expected_languages = ["ru", "es", "fr", "de"]
        self.assertEqual(set(languages), set(expected_languages))  # порядок не важен

    def test_is_text_supported_returns_true_for_known_text(self):
        """TDD Шаг 9: is_text_supported возвращает True для поддерживаемого текста."""
        self.assertTrue(self.translator.is_text_supported("Hello"))
        self.assertTrue(self.translator.is_text_supported("No"))

    def test_is_text_supported_returns_false_for_unknown_text(self):
        """TDD Шаг 10: is_text_supported возвращает False для неизвестного текста."""
        self.assertFalse(self.translator.is_text_supported("Artificial Intelligence"))

    # ============ Дополнительный тест: Перевод на несуществующий язык ============
    def test_translate_to_unsupported_language_returns_original(self):
        """TDD Шаг 11: Перевод на несуществующий язык возвращает исходный текст."""
        # Given: поддерживаемый текст, но несуществующий язык
        result = self.translator.translate("Hello", "jp")  # японский не поддерживается в заглушке

        # Then: возвращается исходный текст
        self.assertEqual(result, "Hello")


if __name__ == "__main__":
    unittest.main(verbosity=2)