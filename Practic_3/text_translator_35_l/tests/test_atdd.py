# tests/test_atdd_translator.py
import unittest
from src.text_translator import TextTranslator

class TestTextTranslatorATDD(unittest.TestCase):
    """
    ATDD-тесты для переводчика текстов.
    Моделируют сценарии использования переводчика с точки зрения пользователя.
    Согласованы с "заказчиком" как приёмочные критерии.
    """

    def setUp(self):
        """Создаём новый переводчик перед каждым тестом."""
        self.translator = TextTranslator()

    # ============ Сценарий 1: Успешный перевод поддерживаемого текста ============
    def test_user_translates_supported_text_successfully(self):
        """
        ATDD Сценарий 1:
        Given: Пользователь вводит текст "Hello" и выбирает язык "ru"
        When: Запрашивает перевод
        Then: Видит результат "Привет"
        And: Система подтверждает, что перевод выполнен успешно
        """
        # Given
        text = "Hello"
        target_lang = "ru"

        # When
        result = self.translator.translate(text, target_lang)

        # Then
        self.assertEqual(result, "Привет", "Перевод должен быть корректным")

        # And: эмулируем отображение сообщения в UI
        success_message = "Перевод выполнен успешно." if result != text else ""
        self.assertEqual(success_message, "Перевод выполнен успешно.")

    # ============ Сценарий 2: Перевод неизвестного текста ============
    def test_user_sees_original_text_and_message_for_unsupported_text(self):
        """
        ATDD Сценарий 2:
        Given: Пользователь вводит текст "Quantum Physics" и выбирает язык "es"
        When: Запрашивает перевод
        Then: Видит результат "Quantum Physics" (исходный текст)
        And: Видит сообщение "Перевод не найден. Показан исходный текст."
        """
        # Given
        text = "Quantum Physics"
        target_lang = "es"

        # When
        result = self.translator.translate(text, target_lang)

        # Then
        self.assertEqual(result, text, "Для неизвестного текста должен возвращаться исходный текст")

        # And: эмулируем отображение сообщения в UI
        warning_message = "Перевод не найден. Показан исходный текст." if result == text else ""
        self.assertEqual(warning_message, "Перевод не найден. Показан исходный текст.")

    # ============ Сценарий 3: Попытка перевода с пустым текстом ============
    def test_user_sees_error_message_when_text_is_empty(self):
        """
        ATDD Сценарий 3:
        Given: Пользователь оставляет поле текста пустым и выбирает язык "fr"
        When: Запрашивает перевод
        Then: Система выбрасывает ValueError
        And: Пользователь видит сообщение "Текст не может быть пустым."
        """
        # Given
        text = ""
        target_lang = "fr"

        # When/Then: ожидаем исключение
        with self.assertRaises(ValueError) as context:
            self.translator.translate(text, target_lang)

        # And: проверяем точное сообщение об ошибке
        self.assertEqual(str(context.exception), "Текст не может быть пустым.")

        # Эмулируем отображение пользователю
        error_message = "Текст не может быть пустым." if str(context.exception) == "Текст не может быть пустым." else ""
        self.assertEqual(error_message, "Текст не может быть пустым.")

    # ============ Сценарий 4: Просмотр списка поддерживаемых языков ============
    def test_user_views_list_of_supported_languages(self):
        """
        ATDD Сценарий 4:
        Given: Пользователь открывает список поддерживаемых языков
        When: Запрашивает get_supported_languages()
        Then: Видит список ['ru', 'es', 'fr', 'de'] (порядок не важен)
        And: Видит сообщение "Доступные языки: русский, испанский, французский, немецкий"
        """
        # When
        languages = self.translator.get_supported_languages()

        # Then
        expected_languages = ["ru", "es", "fr", "de"]
        self.assertEqual(set(languages), set(expected_languages), "Список языков должен совпадать")

        # And: эмулируем отображение пользователю
        language_names = {
            "ru": "русский",
            "es": "испанский",
            "fr": "французский",
            "de": "немецкий"
        }
        display_message = "Доступные языки: " + ", ".join(language_names[lang] for lang in languages)
        expected_display = "Доступные языки: русский, испанский, французский, немецкий"
        self.assertEqual(display_message, expected_display)

    # ============ Сценарий 5: Проверка поддержки текста перед переводом ============
    def test_user_checks_if_text_is_supported_before_translating(self):
        """
        ATDD Сценарий 5:
        Given: Пользователь вводит текст "Yes" и хочет проверить, поддерживается ли его перевод
        When: Вызывает is_text_supported("Yes")
        Then: Получает True
        And: Видит сообщение "Текст поддерживается. Можно перевести."
        """
        # Given
        text = "Yes"

        # When
        is_supported = self.translator.is_text_supported(text)

        # Then
        self.assertTrue(is_supported, "Текст 'Yes' должен поддерживаться")

        # And: эмулируем отображение пользователю
        support_message = "Текст поддерживается. Можно перевести." if is_supported else "Текст не поддерживается. Перевод может быть неточным."
        self.assertEqual(support_message, "Текст поддерживается. Можно перевести.")


if __name__ == "__main__":
    unittest.main(verbosity=2)