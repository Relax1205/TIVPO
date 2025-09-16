# demo_booking.py
from src.restaurant_booking import RestaurantBookingSystem
from datetime import datetime, timedelta

def main():
    # Создаём систему бронирования
    rbs = RestaurantBookingSystem()

    # Текущее время + 1 час (для демонстрации)
    now = datetime.now()
    time1 = (now + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")
    time2 = (now + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M")

    # Бронируем столик 5 на time1
    success1 = rbs.book_table(5, "Иван Петров", time1)
    print(f"✅ Бронирование столика 5 на {time1}: {'Успешно' if success1 else 'Не удалось'}")

    # Пытаемся забронировать тот же столик на то же время
    success2 = rbs.book_table(5, "Мария Сидорова", time1)
    print(f"❌ Повторное бронирование столика 5 на {time1}: {'Успешно' if success2 else 'Не удалось'}")

    # Бронируем столик 3 на time2
    success3 = rbs.book_table(3, "Анна Козлова", time2)
    print(f"✅ Бронирование столика 3 на {time2}: {'Успешно' if success3 else 'Не удалось'}")

    # Отменяем бронирование столика 5
    cancel_success = rbs.cancel_booking(5, time1)
    print(f"🗑️  Отмена бронирования столика 5 на {time1}: {'Успешно' if cancel_success else 'Не удалось'}")

    # Просмотр активных бронирований
    print(f"\n📋 Активные бронирования:")
    active_bookings = rbs.get_active_bookings()
    for booking in active_bookings:
        print(f"   Столик {booking['table_number']} на {booking['booking_time']} — {booking['customer_name']}")

    # Проверка доступности столика 5 на time1 (после отмены)
    available = rbs.is_table_available(5, time1)
    print(f"\n🔍 Столик 5 на {time1} доступен: {available}")


if __name__ == "__main__":
    main()