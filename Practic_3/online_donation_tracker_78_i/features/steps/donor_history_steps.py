# features/steps/donor_history_steps.py
from behave import given, when, then
from src.donation_tracker import DonationTracker

@given('пожертвование зафиксировано с параметрами:')
def step_impl(context):
    context.tracker = DonationTracker()
    for row in context.table:
        context.tracker.log_donation(
            row['donor_name'],
            float(row['amount']),
            row['cause'],
            row['date']
        )

@when('я запрашиваю историю пожертвований для донора "{donor_name}"')
def step_impl(context, donor_name):
    context.donor_history = context.tracker.get_donations_by_donor(donor_name)
    context.requested_donor = donor_name

@then('я вижу данные доноров:')
def step_impl(context):
    expected_table = context.table
    actual_donations = context.donor_history

    # Проверяем количество записей
    assert len(actual_donations) == len(expected_table.rows), \
        f"Ожидалось {len(expected_table.rows)} записей, получено {len(actual_donations)}"

    # Проверяем каждую запись
    for i, expected_row in enumerate(expected_table):
        actual = actual_donations[i]
        assert actual["donor_name"] == expected_row["donor_name"], \
            f"Донор не совпадает: ожидалось {expected_row['donor_name']}, получено {actual['donor_name']}"
        assert abs(actual["amount"] - float(expected_row["amount"])) < 0.01, \
            f"Сумма не совпадает: ожидалось {expected_row['amount']}, получено {actual['amount']}"
        assert actual["cause"] == expected_row["cause"], \
            f"Цель не совпадает: ожидалось {expected_row['cause']}, получено {actual['cause']}"
        assert actual["date"] == expected_row["date"], \
            f"Дата не совпадает: ожидалось {expected_row['date']}, получено {actual['date']}"