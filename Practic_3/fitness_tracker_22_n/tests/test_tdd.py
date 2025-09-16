# tests/test_tdd.py
import unittest
from datetime import datetime, timedelta
from src.fitness_tracker import FitnessTracker

class TestFitnessTrackerTDD(unittest.TestCase):
    """
    TDD-тесты для фитнес-трекера.
    Покрывают логирование тренировок и расчёт статистики.
    """

    def setUp(self):
        """Создаём новый трекер перед каждым тестом."""
        self.tracker = FitnessTracker()

    # ============ Этап 1: Тесты для ЛОГИРОВАНИЯ (должны падать без реализации) ============
    def test_log_workout_records_data(self):
        """TDD Шаг 1: Проверяем, что log_workout сохраняет тренировку."""
        # Given: нет тренировок
        self.assertEqual(len(self.tracker.get_all_workouts()), 0)

        # When: логируем тренировку
        self.tracker.log_workout("2025-04-01", 5000, 300.0, 40)

        # Then: появилась 1 тренировка с правильными данными
        workouts = self.tracker.get_all_workouts()
        self.assertEqual(len(workouts), 1)
        self.assertEqual(workouts[0]["date"], "2025-04-01")
        self.assertEqual(workouts[0]["steps"], 5000)
        self.assertEqual(workouts[0]["calories"], 300.0)
        self.assertEqual(workouts[0]["duration_min"], 40)

    # ============ Этап 2: Тесты для РАСЧЁТА СТАТИСТИКИ (должны падать без реализации) ============
    def test_statistics_empty_no_workouts(self):
        """TDD Шаг 2: Если нет тренировок — статистика нулевая."""
        # Given: трекер пуст
        # When: запрашиваем статистику за 7 дней (фиксируем "сегодня" для детерминизма)
        stats = self.tracker.get_statistics(7, "2025-04-08")

        # Then: все значения нулевые
        self.assertEqual(stats["total_workouts"], 0)
        self.assertEqual(stats["total_steps"], 0)
        self.assertEqual(stats["total_calories"], 0.0)
        self.assertEqual(stats["avg_steps_per_day"], 0)
        self.assertEqual(stats["avg_calories_per_day"], 0.0)
        self.assertEqual(stats["goal_progress"], {})

    def test_statistics_calculates_correctly_for_one_workout(self):
        """TDD Шаг 3: Статистика корректно считается для одной тренировки."""
        # Given: одна тренировка в пределах периода
        self.tracker.log_workout("2025-04-07", 8000, 450.5, 45)  # вчера, если сегодня 2025-04-08

        # When: запрашиваем статистику за 7 дней
        stats = self.tracker.get_statistics(7, "2025-04-08")

        # Then: статистика отражает одну тренировку
        self.assertEqual(stats["total_workouts"], 1)
        self.assertEqual(stats["total_steps"], 8000)
        self.assertEqual(stats["total_calories"], 450.5)
        self.assertEqual(stats["avg_steps_per_day"], 8000 // 7)  # 1142
        self.assertAlmostEqual(stats["avg_calories_per_day"], 450.5 / 7, places=2)  # ~64.36

    def test_statistics_ignores_workouts_outside_period(self):
        """TDD Шаг 4: Тренировки за пределами периода не учитываются."""
        # Given: одна тренировка внутри периода, одна — снаружи
        self.tracker.log_workout("2025-04-01", 10000, 600.0, 60)  # слишком давно (если сегодня 2025-04-08)
        self.tracker.log_workout("2025-04-07", 5000, 300.0, 30)   # вчера — попадает в период

        # When: запрашиваем статистику за 7 дней
        stats = self.tracker.get_statistics(7, "2025-04-08")

        # Then: учитывается только последняя тренировка
        self.assertEqual(stats["total_workouts"], 1)
        self.assertEqual(stats["total_steps"], 5000)
        self.assertEqual(stats["total_calories"], 300.0)

    def test_statistics_calculates_goal_progress(self):
        """TDD Шаг 5: Статистика корректно рассчитывает прогресс по целям."""
        # Given: установлена цель + есть тренировки в периоде
        self.tracker.set_goal("steps", 35000)
        self.tracker.set_goal("calories", 2500)

        self.tracker.log_workout("2025-04-06", 10000, 600.0, 60)
        self.tracker.log_workout("2025-04-07", 15000, 900.0, 90)
        self.tracker.log_workout("2025-04-08", 12000, 720.0, 72)  # сегодня

        # When: запрашиваем статистику за 7 дней (включая сегодня)
        stats = self.tracker.get_statistics(7, "2025-04-08")

        # Then: прогресс по целям рассчитан верно
        goal_progress = stats["goal_progress"]

        # Проверка шагов: 10000 + 15000 + 12000 = 37000
        self.assertIn("steps", goal_progress)
        self.assertEqual(goal_progress["steps"]["target"], 35000)
        self.assertEqual(goal_progress["steps"]["actual"], 37000)
        self.assertAlmostEqual(goal_progress["steps"]["progress_percent"], 105.71, places=2)

        # Проверка калорий: 600 + 900 + 720 = 2220
        self.assertIn("calories", goal_progress)
        self.assertEqual(goal_progress["calories"]["target"], 2500)
        self.assertEqual(goal_progress["calories"]["actual"], 2220.0)
        self.assertAlmostEqual(goal_progress["calories"]["progress_percent"], 88.8, places=2)

    def test_log_workout_with_invalid_data_raises_no_error_but_stores_as_is(self):
        """TDD Шаг 6 (Граничный случай): Логирование с нулевыми/отрицательными значениями."""
        # Given: ничего
        # When: логируем "неправдоподобную" тренировку
        self.tracker.log_workout("2025-04-08", 0, -100.0, -10)

        # Then: данные сохранены "как есть" (можно добавить валидацию позже в рефакторинге)
        workouts = self.tracker.get_all_workouts()
        self.assertEqual(len(workouts), 1)
        self.assertEqual(workouts[0]["steps"], 0)
        self.assertEqual(workouts[0]["calories"], -100.0)
        self.assertEqual(workouts[0]["duration_min"], -10)


if __name__ == "__main__":
    unittest.main(verbosity=2)