# demo.py
from src.donation_tracker import DonationTracker

def main():
    # Создаём трекер
    tracker = DonationTracker()

    # Логируем пожертвования
    tracker.log_donation("Анна Петрова", 1500.0, "Помощь детям", "2025-04-01")
    tracker.log_donation("Иван Смирнов", 3000.0, "Экология", "2025-04-02")
    tracker.log_donation("Анна Петрова", 500.0, "Помощь детям", "2025-04-03")
    tracker.log_donation("Ольга Козлова", 2000.0, "Экология", "2025-04-04")
    tracker.log_donation("Иван Смирнов", 1000.0, "Помощь животным", "2025-04-05")

    # Получаем список доноров
    donors = tracker.get_all_donors()
    print("👥 Список доноров:")
    for donor in donors:
        print(f" - {donor}")

    # Генерируем общий отчёт
    report = tracker.generate_report()
    print("\n📊 Общий отчёт:")
    print(f"Всего пожертвований: {report['total_donations']}")
    print(f"Общая сумма: {report['total_amount']} руб.")
    print(f"Уникальных доноров: {report['unique_donors']}")
    print(f"Топ-донор: {report['top_donor']}")
    print("\n📈 Сводка по целям:")
    for cause, amount in report["causes_summary"].items():
        print(f" - {cause}: {amount} руб.")

    # Получаем историю по конкретному донору
    anna_donations = tracker.get_donations_by_donor("Анна Петрова")
    print(f"\n📋 Пожертвования Анны Петровой:")
    for donation in anna_donations:
        print(f" - {donation['date']}: {donation['amount']} руб. на '{donation['cause']}'")


if __name__ == "__main__":
    main()