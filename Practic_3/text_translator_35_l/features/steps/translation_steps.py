from behave import given, when, then
from src.text_translator import TextTranslator

@given('текст "{text}" введён для перевода')
def step_impl(context, text):
    """
    Инициализирует переводчик и сохраняет текст в контексте.
    """
    context.translator = TextTranslator()
    context.input_text = text

# 👇 ДОБАВЬТЕ ЭТОТ ШАГ 👇
@given('текст "" введён для перевода')
def step_impl(context):
    """
    Специальный шаг для обработки пустого текста.
    """
    context.translator = TextTranslator()
    context.input_text = ""

@when('я выбираю язык "{target_lang}"')
def step_impl(context, target_lang):
    """
    Выполняет попытку перевода и сохраняет результат в контексте.
    """
    context.target_language = target_lang
    try:
        context.translated_text = context.translator.translate(context.input_text, target_lang)
        context.error_occurred = False
    except ValueError as e:
        context.error_message = str(e)
        context.error_occurred = True

@then('я вижу переведённый текст "{expected_text}"')
def step_impl(context, expected_text):
    """
    Проверяет, что результат перевода совпадает с ожидаемым.
    """
    assert not context.error_occurred, "Не ожидалось возникновение ошибки"
    assert context.translated_text == expected_text, \
        f'Ожидалось: "{expected_text}", получено: "{context.translated_text}"'

@then('система показывает сообщение "{expected_message}"')
def step_impl(context, expected_message):
    """
    Проверяет, что система выдала ожидаемое сообщение об ошибке.
    """
    assert context.error_occurred, "Ожидалась ошибка, но она не возникла"
    assert expected_message in context.error_message, \
        f'Ожидалось сообщение: "{expected_message}", получено: "{context.error_message}"'