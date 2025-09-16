# features/steps/password_steps.py
from behave import given, when, then
from src.password_manager import PasswordManager

@given('пароль сохранён для сервиса "{service_name}" с логином "{login}" и паролем "{password}"')
def step_impl(context, service_name, login, password):
    context.pm = PasswordManager()
    context.pm.save_password(service_name, login, password)

@when('я запрашиваю доступ к паролю для сервиса "{service_name}"')
def step_impl(context, service_name):
    context.requested_service = service_name
    context.retrieved_data = context.pm.get_password(service_name)

@then('я получаю пароль "{expected_password}" и логин "{expected_login}"')
def step_impl(context, expected_password, expected_login):
    assert context.retrieved_data is not None, f"Пароль для сервиса '{context.requested_service}' не найден"
    assert context.retrieved_data["password"] == expected_password, \
        f"Ожидался пароль '{expected_password}', получен '{context.retrieved_data['password']}'"
    assert context.retrieved_data["login"] == expected_login, \
        f"Ожидался логин '{expected_login}', получен '{context.retrieved_data['login']}'"