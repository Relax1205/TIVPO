# demo_translator.py
from src.text_translator import TextTranslator

def main():
    # Создаём переводчик
    translator = TextTranslator()

    # Примеры текстов для перевода
    texts = ["Hello", "Goodbye", "Thank you", "Yes", "No", "Unsupported Text"]

    # Поддерживаемые языки
    languages = translator.get_supported_languages()
    print(f"🌍 Поддерживаемые языки: {languages}\n")

    # Переводим каждый текст на все поддерживаемые языки
    for text in texts:
        print(f'🔤 Исходный текст: "{text}"')
        for lang in languages:
            translated = translator.translate(text, lang)
            print(f'   → {lang}: "{translated}"')
        print()  # пустая строка для разделения


if __name__ == "__main__":
    main()