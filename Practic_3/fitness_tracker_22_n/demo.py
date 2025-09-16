# demo.py
from src.fitness_tracker import FitnessTracker

def main():
    tracker = FitnessTracker()
    
    # Установка целей
    tracker.set_goal("steps", 35000)    # 35к шагов за неделю
    tracker.set_goal("calories", 2500)  # 2500 калорий за неделю

    # Логирование тренировок (в прошлом относительно "сегодня" 2025-04-06)
    tracker.log_workout("2025-04-01", 8000, 450.5, 45)
    tracker.log_workout("2025-04-02", 10000, 600.0, 60)
    tracker.log_workout("2025-04-05", 9000, 550.0, 55)

    # Получение статистики за неделю, считая, что сегодня 2025-04-06
    stats = tracker.get_statistics(7, "2025-04-06")
    print("📊 Статистика за неделю (на 2025-04-06):")
    for key, value in stats.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()