# src/fitness_tracker.py
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class FitnessTracker:
    """
    Класс для отслеживания фитнес-активности пользователя.
    Позволяет логировать тренировки, устанавливать цели и просматривать статистику.
    """

    def __init__(self):
        self.workouts: List[Dict] = []  # Список тренировок
        self.goals: Dict[str, float] = {}  # Цели (например, "steps": 10000, "calories": 2000)

    def log_workout(self, date: str, steps: int, calories: float, duration_min: int) -> None:
        """
        Логирует новую тренировку.
        
        :param date: Дата тренировки в формате 'YYYY-MM-DD'
        :param steps: Количество шагов
        :param calories: Сожженные калории
        :param duration_min: Продолжительность в минутах
        """
        workout = {
            "date": date,
            "steps": steps,
            "calories": calories,
            "duration_min": duration_min
        }
        self.workouts.append(workout)

    def set_goal(self, metric: str, target: float) -> None:
        """
        Устанавливает цель для указанной метрики.
        
        :param metric: Метрика (например, 'steps', 'calories')
        :param target: Целевое значение
        """
        self.goals[metric] = target

    def get_statistics(self, period_days: int = 7, current_date_str: Optional[str] = None) -> Dict:
        """
        Возвращает статистику за последние N дней.
        
        :param period_days: Количество дней для анализа (по умолчанию 7)
        :param current_date_str: Текущая дата в формате 'YYYY-MM-DD' (для тестов). 
                                Если None — используется datetime.now().
        :return: Словарь со статистикой
        """
        if current_date_str:
            current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
        else:
            current_date = datetime.now()

        # Приводим current_date к началу дня
        current_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
        cutoff_date = current_date - timedelta(days=period_days)

        # Включаем только тренировки, которые строго ПОЗЖЕ cutoff_date
        recent_workouts = [
            w for w in self.workouts
            if datetime.strptime(w["date"], "%Y-%m-%d") > cutoff_date
        ]

        if not recent_workouts:
            return {
                "total_workouts": 0,
                "total_steps": 0,
                "total_calories": 0.0,
                "avg_steps_per_day": 0,
                "avg_calories_per_day": 0.0,
                "goal_progress": {}
            }

        total_steps = sum(w["steps"] for w in recent_workouts)
        total_calories = sum(w["calories"] for w in recent_workouts)
        total_workouts = len(recent_workouts)

        avg_steps_per_day = total_steps // period_days
        avg_calories_per_day = total_calories / period_days

        # Рассчитываем прогресс по целям
        goal_progress = {}
        for metric, target in self.goals.items():
            if metric == "steps":
                actual = total_steps
            elif metric == "calories":
                actual = total_calories
            else:
                continue  # Пропускаем неизвестные метрики
            progress_percent = (actual / target * 100) if target > 0 else 0
            goal_progress[metric] = {
                "target": target,
                "actual": actual,
                "progress_percent": round(progress_percent, 2)
            }

        return {
            "total_workouts": total_workouts,
            "total_steps": total_steps,
            "total_calories": round(total_calories, 2),
            "avg_steps_per_day": avg_steps_per_day,
            "avg_calories_per_day": round(avg_calories_per_day, 2),
            "goal_progress": goal_progress
        }

    def get_all_workouts(self) -> List[Dict]:
        """
        Возвращает полный список всех тренировок.
        Полезно для отладки или отображения истории.
        """
        return self.workouts.copy()