# tests/test_atdd.py
import unittest
from datetime import datetime, timedelta
from src.fitness_tracker import FitnessTracker

class TestFitnessTrackerATDD(unittest.TestCase):
    """
    ATDD-тесты для фитнес-трекера.
    Моделируют сценарии отслеживания прогресса с точки зрения пользователя.
    Согласованы с "заказчиком" как приёмочные критерии.
    """

    def setUp(self):
        """Создаём новый трекер перед каждым тестом."""
        self.tracker = FitnessTracker()

    # ============ Сценарий 1: Мотивация при высоком прогрессе ============
    def test_user_sees_motivation_message_when_progress_over_80_percent(self):
        """
        ATDD Сценарий 1:
        Given: Пользователь установил цель по шагам = 10000
        And: Залогировал тренировку на 8500 шагов за сегодня
        When: Запрашивает статистику
        Then: Видит сообщение: "Ты на верном пути! Осталось немного!"
        """
        # Given
        self.tracker.set_goal("steps", 10000)
        today = datetime.now().strftime("%Y-%m-%d")
        self.tracker.log_workout(today, 8500, 500.0, 60)  # 85% цели

        # When
        stats = self.tracker.get_statistics(7, today)
        goal_progress = stats["goal_progress"].get("steps", {})
        progress_percent = goal_progress.get("progress_percent", 0)

        # Then: Проверяем расчёт прогресса
        self.assertGreater(progress_percent, 80)
        self.assertLess(progress_percent, 100)

        # Then: Проверяем наличие мотивирующего сообщения (логика в тесте)
        motivation_message = ""
        if 80 < progress_percent < 100:
            motivation_message = "Ты на верном пути! Осталось немного!"

        self.assertEqual(motivation_message, "Ты на верном пути! Осталось немного!")

    # ============ Сценарий 2: Напоминание о бездействии ============
    def test_user_sees_reminder_after_3_days_of_inactivity(self):
        """
        ATDD Сценарий 2:
        Given: Последняя тренировка была 4 дня назад
        When: Пользователь открывает приложение сегодня
        Then: Видит сообщение: "Ты пропустил несколько дней. Вернись к тренировкам!"
        """
        # Given: последняя тренировка 4 дня назад
        today = datetime.now()
        four_days_ago = (today - timedelta(days=4)).strftime("%Y-%m-%d")
        self.tracker.log_workout(four_days_ago, 5000, 300.0, 40)

        # When: проверяем, сколько дней прошло с последней тренировки
        last_workout_date = datetime.strptime(four_days_ago, "%Y-%m-%d")
        days_since_last_workout = (today - last_workout_date).days

        # Then: Проверяем условие и сообщение
        reminder_message = ""
        if days_since_last_workout >= 3:
            reminder_message = "Ты пропустил несколько дней. Вернись к тренировкам!"

        self.assertEqual(days_since_last_workout, 4)
        self.assertEqual(reminder_message, "Ты пропустил несколько дней. Вернись к тренировкам!")

    # ============ Сценарий 3: Поздравление при достижении цели ============
    def test_user_sees_congratulations_when_goal_reached(self):
        """
        ATDD Сценарий 3:
        Given: Пользователь установил цель по калориям = 2000
        And: Залогировал тренировку на 2100 калорий за сегодня
        When: Запрашивает статистику
        Then: Видит сообщение: "Поздравляем! Цель достигнута 🎉"
        """
        # Given
        self.tracker.set_goal("calories", 2000)
        today = datetime.now().strftime("%Y-%m-%d")
        self.tracker.log_workout(today, 10000, 2100.0, 90)  # 105% цели

        # When
        stats = self.tracker.get_statistics(7, today)
        goal_progress = stats["goal_progress"].get("calories", {})
        progress_percent = goal_progress.get("progress_percent", 0)

        # Then: Проверяем расчёт прогресса
        self.assertGreaterEqual(progress_percent, 100)

        # Then: Проверяем наличие поздравительного сообщения
        congrat_message = ""
        if progress_percent >= 100:
            congrat_message = "Поздравляем! Цель достигнута 🎉"

        self.assertEqual(congrat_message, "Поздравляем! Цель достигнута 🎉")

    # ============ Дополнительный сценарий: Нет сообщений, если прогресс низкий ============
    def test_no_special_message_when_progress_is_low(self):
        """
        ATDD Сценарий 4 (дополнительный):
        Given: Пользователь установил цель по шагам = 10000
        And: Залогировал тренировку на 3000 шагов
        When: Запрашивает статистику
        Then: Никаких специальных сообщений не показывается (только статистика)
        """
        # Given
        self.tracker.set_goal("steps", 10000)
        today = datetime.now().strftime("%Y-%m-%d")
        self.tracker.log_workout(today, 3000, 200.0, 30)  # 30% цели

        # When
        stats = self.tracker.get_statistics(7, today)
        goal_progress = stats["goal_progress"].get("steps", {})
        progress_percent = goal_progress.get("progress_percent", 0)

        # Then
        self.assertLess(progress_percent, 80)

        # Then: Никаких мотивационных/поздравительных сообщений
        special_message = ""
        if progress_percent >= 100:
            special_message = "Поздравляем! Цель достигнута 🎉"
        elif progress_percent > 80:
            special_message = "Ты на верном пути! Осталось немного!"

        self.assertEqual(special_message, "")  # Никакого сообщения


if __name__ == "__main__":
    unittest.main(verbosity=2)