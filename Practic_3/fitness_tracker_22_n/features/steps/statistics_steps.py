# features/steps/statistics_steps.py
from behave import given, when, then
from src.fitness_tracker import FitnessTracker

@given('тренировка записана с параметрами:')
def step_impl(context):
    context.tracker = FitnessTracker()
    for row in context.table:
        context.tracker.log_workout(
            row['date'],
            int(row['steps']),
            float(row['calories']),
            int(row['duration'])
        )

@when('я запрашиваю статистику за {period:d} дней на дату "{current_date}"')
def step_impl(context, period, current_date):
    context.stats = context.tracker.get_statistics(period, current_date)

@then('я вижу корректный результат:')
def step_impl(context):
    expected = context.table[0]  # Берём первую строку таблицы
    actual = context.stats

    assert actual["total_workouts"] == int(expected["total_workouts"]), \
        f"Ожидалось total_workouts={expected['total_workouts']}, получено {actual['total_workouts']}"

    assert actual["total_steps"] == int(expected["total_steps"]), \
        f"Ожидалось total_steps={expected['total_steps']}, получено {actual['total_steps']}"

    assert abs(actual["total_calories"] - float(expected["total_calories"])) < 0.01, \
        f"Ожидалось total_calories={expected['total_calories']}, получено {actual['total_calories']}"

    assert actual["avg_steps_per_day"] == int(expected["avg_steps_per_day"]), \
        f"Ожидалось avg_steps_per_day={expected['avg_steps_per_day']}, получено {actual['avg_steps_per_day']}"

    assert abs(actual["avg_calories_per_day"] - float(expected["avg_calories_per_day"])) < 0.01, \
        f"Ожидалось avg_calories_per_day={expected['avg_calories_per_day']}, получено {actual['avg_calories_per_day']}"