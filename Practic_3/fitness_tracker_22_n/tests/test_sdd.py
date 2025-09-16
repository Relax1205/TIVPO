# tests/test_sdd.py
import unittest
from src.fitness_tracker import FitnessTracker

class TestFitnessTrackerSDD(unittest.TestCase):
    """
    SDD-тесты для фитнес-трекера.
    На основе спецификации с примерами тренировок и ожидаемыми расчётами.
    Таблица спецификации находится в specs/workout_examples.md
    """

    def setUp(self):
        """Создаём новый трекер перед каждым тестом."""
        self.tracker = FitnessTracker()
        # Устанавливаем цели, как в спецификации
        self.tracker.set_goal("steps", 35000)
        self.tracker.set_goal("calories", 2500)

    def test_sdd_specification_example_1(self):
        """
        SDD Пример 1 (из таблицы):
        Given: тренировка от 2025-04-01 (5000 шагов, 300.0 калорий)
        When: запрашиваю статистику на дату "2025-04-07" за 7 дней
        Then: вижу ожидаемые значения из спецификации
        """
        # Given
        self.tracker.log_workout("2025-04-01", 5000, 300.0, 30)

        # When
        stats = self.tracker.get_statistics(7, "2025-04-07")

        # Then — сверяем с ожиданиями из таблицы
        self.assertEqual(stats["total_steps"], 5000)
        self.assertAlmostEqual(stats["total_calories"], 300.0, places=2)
        self.assertEqual(stats["avg_steps_per_day"], 5000 // 7)  # 714
        self.assertAlmostEqual(stats["avg_calories_per_day"], 300.0 / 7, places=2)  # 42.86

        # Проверка прогресса по целям
        steps_progress = stats["goal_progress"]["steps"]["progress_percent"]
        calories_progress = stats["goal_progress"]["calories"]["progress_percent"]
        self.assertAlmostEqual(steps_progress, 14.29, places=2)
        self.assertAlmostEqual(calories_progress, 12.00, places=2)

    def test_sdd_specification_example_2(self):
        """
        SDD Пример 2 (из таблицы):
        Given: тренировки от 2025-04-01, 2025-04-05
        When: запрашиваю статистику на дату "2025-04-07" за 7 дней
        Then: вижу ожидаемые значения из спецификации
        """
        # Given
        self.tracker.log_workout("2025-04-01", 5000, 300.0, 30)
        self.tracker.log_workout("2025-04-05", 8000, 480.0, 48)

        # When
        stats = self.tracker.get_statistics(7, "2025-04-07")

        # Then
        self.assertEqual(stats["total_steps"], 13000)
        self.assertAlmostEqual(stats["total_calories"], 780.0, places=2)
        self.assertEqual(stats["avg_steps_per_day"], 13000 // 7)  # 1857
        self.assertAlmostEqual(stats["avg_calories_per_day"], 780.0 / 7, places=2)  # 111.43

        steps_progress = stats["goal_progress"]["steps"]["progress_percent"]
        calories_progress = stats["goal_progress"]["calories"]["progress_percent"]
        self.assertAlmostEqual(steps_progress, 37.14, places=2)
        self.assertAlmostEqual(calories_progress, 31.20, places=2)

    def test_sdd_specification_example_3(self):
        """
        SDD Пример 3 (из таблицы):
        Given: тренировки от 2025-04-01, 2025-04-05, 2025-04-06
        When: запрашиваю статистику на дату "2025-04-07" за 7 дней
        Then: вижу ожидаемые значения из спецификации
        """
        # Given
        self.tracker.log_workout("2025-04-01", 5000, 300.0, 30)
        self.tracker.log_workout("2025-04-05", 8000, 480.0, 48)
        self.tracker.log_workout("2025-04-06", 7000, 420.0, 42)

        # When
        stats = self.tracker.get_statistics(7, "2025-04-07")

        # Then
        self.assertEqual(stats["total_steps"], 20000)
        self.assertAlmostEqual(stats["total_calories"], 1200.0, places=2)
        self.assertEqual(stats["avg_steps_per_day"], 20000 // 7)  # 2857
        self.assertAlmostEqual(stats["avg_calories_per_day"], 1200.0 / 7, places=2)  # 171.43

        steps_progress = stats["goal_progress"]["steps"]["progress_percent"]
        calories_progress = stats["goal_progress"]["calories"]["progress_percent"]
        self.assertAlmostEqual(steps_progress, 57.14, places=2)
        self.assertAlmostEqual(calories_progress, 48.00, places=2)

    def test_sdd_specification_example_4(self):
        """
        SDD Пример 4 (из таблицы):
        Given: тренировки от 2025-04-01, 2025-04-05, 2025-04-06, 2025-04-07
        When: запрашиваю статистику на дату "2025-04-07" за 7 дней
        Then: вижу ожидаемые значения из спецификации
        """
        # Given
        self.tracker.log_workout("2025-04-01", 5000, 300.0, 30)
        self.tracker.log_workout("2025-04-05", 8000, 480.0, 48)
        self.tracker.log_workout("2025-04-06", 7000, 420.0, 42)
        self.tracker.log_workout("2025-04-07", 10000, 600.0, 60)

        # When
        stats = self.tracker.get_statistics(7, "2025-04-07")

        # Then
        self.assertEqual(stats["total_steps"], 30000)
        self.assertAlmostEqual(stats["total_calories"], 1800.0, places=2)
        self.assertEqual(stats["avg_steps_per_day"], 30000 // 7)  # 4285
        self.assertAlmostEqual(stats["avg_calories_per_day"], 1800.0 / 7, places=2)  # 257.14

        steps_progress = stats["goal_progress"]["steps"]["progress_percent"]
        calories_progress = stats["goal_progress"]["calories"]["progress_percent"]
        self.assertAlmostEqual(steps_progress, 85.71, places=2)
        self.assertAlmostEqual(calories_progress, 72.00, places=2)


if __name__ == "__main__":
    unittest.main(verbosity=2)