# features/steps/finance_steps.py
from behave import given, when, then
from src.finance_manager import FinanceManager

@given('доходы и расходы внесены:')
def step_impl(context):
    """
    Инициализирует FinanceManager и добавляет транзакции из таблицы.
    """
    context.fm = FinanceManager()
    for row in context.table:
        context.fm.add_transaction(
            amount=float(row['amount']),
            category=row['category'],
            transaction_type=row['type'],
            date_str=row['date']
        )

@when('я генерирую финансовый отчёт')
def step_impl(context):
    """
    Генерирует отчёт и сохраняет его в контексте.
    """
    context.report = context.fm.generate_report()

@then('баланс рассчитывается корректно и равен {expected_balance:f}')
def step_impl(context, expected_balance):
    """
    Проверяет, что баланс в отчёте совпадает с ожидаемым.
    """
    actual_balance = context.report["balance"]
    assert abs(actual_balance - expected_balance) < 0.01, \
        f"Ожидался баланс {expected_balance}, получен {actual_balance}"

@then('в отчёте отображаются корректные суммы доходов ({expected_income:f}) и расходов ({expected_expense:f})')
def step_impl(context, expected_income, expected_expense):
    """
    Проверяет суммы доходов и расходов в отчёте.
    """
    actual_income = context.report["total_income"]
    actual_expense = context.report["total_expense"]

    assert abs(actual_income - expected_income) < 0.01, \
        f"Ожидалась сумма доходов {expected_income}, получена {actual_income}"
    assert abs(actual_expense - expected_expense) < 0.01, \
        f"Ожидалась сумма расходов {expected_expense}, получена {actual_expense}"