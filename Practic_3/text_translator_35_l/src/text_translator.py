# src/text_translator.py
from typing import Dict, Optional

class TextTranslator:
    """
    Простой переводчик текстов с использованием заглушки (mock).
    Поддерживает перевод ограниченного набора фраз на несколько языков.
    """

    def __init__(self):
        # Заглушка: словарь переводов
        self.translations: Dict[str, Dict[str, str]] = {
            "Hello": {
                "ru": "Привет",
                "es": "Hola",
                "fr": "Bonjour",
                "de": "Hallo"
            },
            "Goodbye": {
                "ru": "До свидания",
                "es": "Adiós",
                "fr": "Au revoir",
                "de": "Auf Wiedersehen"
            },
            "Thank you": {
                "ru": "Спасибо",
                "es": "Gracias",
                "fr": "Merci",
                "de": "Danke"
            },
            "Yes": {
                "ru": "Да",
                "es": "Sí",
                "fr": "Oui",
                "de": "Ja"
            },
            "No": {
                "ru": "Нет",
                "es": "No",
                "fr": "Non",
                "de": "Nein"
            }
        }

    def translate(self, text: str, target_lang: str) -> str:
        """
        Переводит текст на указанный язык.
        
        :param text: Исходный текст
        :param target_lang: Целевой язык (например, 'ru', 'es', 'fr', 'de')
        :return: Переведённый текст. Если перевод не найден — возвращает исходный текст.
        """
        if not text:
            raise ValueError("Текст не может быть пустым.")
        if not target_lang:
            raise ValueError("Язык не может быть пустым.")

        # Ищем перевод в заглушке
        if text in self.translations and target_lang in self.translations[text]:
            return self.translations[text][target_lang]
        
        # Если перевод не найден — возвращаем исходный текст
        return text


    def get_supported_languages(self) -> list:
        """
        Возвращает список поддерживаемых языков.
        
        :return: Список кодов языков
        """
        if not self.translations:
            return []
        # Берём языки из первого доступного текста
        sample_text = next(iter(self.translations))
        return list(self.translations[sample_text].keys())

    def is_text_supported(self, text: str) -> bool:
        """
        Проверяет, поддерживается ли перевод для данного текста.
        
        :param text: Исходный текст
        :return: True, если перевод доступен
        """
        return text in self.translations