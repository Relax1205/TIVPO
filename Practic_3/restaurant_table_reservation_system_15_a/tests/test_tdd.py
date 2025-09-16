# tests/test_tdd_booking.py
import unittest
from datetime import datetime, timedelta
from src.restaurant_booking import RestaurantBookingSystem

class TestRestaurantBookingSystemTDD(unittest.TestCase):
    """
    TDD-тесты для системы бронирования столиков в ресторане.
    Покрывают бронирование, отмену и проверку пересечений.
    """

    def setUp(self):
        """Создаём новую систему бронирования перед каждым тестом."""
        self.rbs = RestaurantBookingSystem()

    # ============ Этап 1: Тесты для БРОНИРОВАНИЯ ============
    def test_book_table_successfully(self):
        """TDD Шаг 1: Успешное бронирование столика на свободное время."""
        # Given: текущее время + 1 час
        booking_time = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")

        # When: бронируем столик
        success = self.rbs.book_table(5, "Иван Петров", booking_time)

        # Then: бронирование успешно
        self.assertTrue(success)

        # Then: бронирование появилось в списке активных
        active_bookings = self.rbs.get_active_bookings()
        self.assertEqual(len(active_bookings), 1)
        self.assertEqual(active_bookings[0]["table_number"], 5)
        self.assertEqual(active_bookings[0]["customer_name"], "Иван Петров")
        self.assertEqual(active_bookings[0]["booking_time"], booking_time)
        self.assertEqual(active_bookings[0]["status"], "confirmed")

    def test_book_table_fails_when_already_booked(self):
        """TDD Шаг 2: Попытка забронировать уже занятый столик на то же время — должна провалиться."""
        # Given: бронируем столик 5 на время X
        booking_time = (datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M")
        self.rbs.book_table(5, "Анна Сидорова", booking_time)

        # When: пытаемся забронировать тот же столик на то же время
        success = self.rbs.book_table(5, "Мария Козлова", booking_time)

        # Then: бронирование неуспешно
        self.assertFalse(success)

        # Then: в списке активных только одна запись
        active_bookings = self.rbs.get_active_bookings()
        self.assertEqual(len(active_bookings), 1)
        self.assertEqual(active_bookings[0]["customer_name"], "Анна Сидорова")

    def test_book_table_with_empty_fields_raises_error(self):
        """TDD Шаг 3: Попытка бронирования с пустыми полями вызывает ValueError."""
        booking_time = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")

        # Then/When: ожидаем исключение для пустого table_number
        with self.assertRaises(ValueError):
            self.rbs.book_table(0, "Иван", booking_time)

        # Then/When: ожидаем исключение для пустого customer_name
        with self.assertRaises(ValueError):
            self.rbs.book_table(5, "", booking_time)

        # Then/When: ожидаем исключение для пустого booking_time
        with self.assertRaises(ValueError):
            self.rbs.book_table(5, "Иван", "")

    def test_book_table_in_past_raises_error(self):
        """TDD Шаг 4: Попытка забронировать столик на прошедшее время вызывает ValueError."""
        # Given: время в прошлом
        past_time = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")

        # When/Then: ожидаем исключение
        with self.assertRaises(ValueError) as context:
            self.rbs.book_table(5, "Иван", past_time)

        self.assertIn("прошедшее время", str(context.exception))

    # ============ Этап 2: Тесты для ОТМЕНЫ БРОНИРОВАНИЯ ============
    def test_cancel_booking_successfully(self):
        """TDD Шаг 5: Успешная отмена существующего бронирования."""
        # Given: бронируем столик
        booking_time = (datetime.now() + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M")
        self.rbs.book_table(7, "Ольга Иванова", booking_time)

        # When: отменяем бронирование
        success = self.rbs.cancel_booking(7, booking_time)

        # Then: отмена успешна
        self.assertTrue(success)

        # Then: в списке активных бронирований запись отсутствует
        active_bookings = self.rbs.get_active_bookings()
        self.assertEqual(len(active_bookings), 0)

        # Then: но в полном списке запись есть со статусом "cancelled"
        all_bookings = self.rbs.get_all_bookings()
        self.assertEqual(len(all_bookings), 1)
        self.assertEqual(all_bookings[0]["status"], "cancelled")

    def test_cancel_nonexistent_booking_returns_false(self):
        """TDD Шаг 6: Попытка отменить несуществующее бронирование возвращает False."""
        # Given: ничего не бронировали
        booking_time = (datetime.now() + timedelta(hours=4)).strftime("%Y-%m-%d %H:%M")

        # When: пытаемся отменить
        success = self.rbs.cancel_booking(8, booking_time)

        # Then: возвращается False
        self.assertFalse(success)

    # ============ Этап 3: Тесты для ПРОВЕРКИ ПЕРЕСЕЧЕНИЙ ============
    def test_is_table_available_returns_true_for_free_slot(self):
        """TDD Шаг 7: is_table_available возвращает True для свободного столика и времени."""
        # Given: бронируем столик 10 на время X
        time1 = (datetime.now() + timedelta(hours=5)).strftime("%Y-%m-%d %H:%M")
        self.rbs.book_table(10, "Алексей", time1)

        # Given: проверяем другое время для того же столика
        time2 = (datetime.now() + timedelta(hours=6)).strftime("%Y-%m-%d %H:%M")

        # When: проверяем доступность
        available = self.rbs.is_table_available(10, time2)

        # Then: столик свободен
        self.assertTrue(available)

    def test_is_table_available_returns_false_for_booked_slot(self):
        """TDD Шаг 8: is_table_available возвращает False для занятого столика и времени."""
        # Given: бронируем столик 10 на время X
        booking_time = (datetime.now() + timedelta(hours=7)).strftime("%Y-%m-%d %H:%M")
        self.rbs.book_table(10, "Алексей", booking_time)

        # When: проверяем то же время
        available = self.rbs.is_table_available(10, booking_time)

        # Then: столик занят
        self.assertFalse(available)

    def test_different_tables_can_be_booked_at_same_time(self):
        """TDD Шаг 9: Разные столики можно бронировать на одно и то же время."""
        # Given: время бронирования
        booking_time = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")

        # When: бронируем столик 1
        success1 = self.rbs.book_table(1, "Гость 1", booking_time)
        # When: бронируем столик 2 на то же время
        success2 = self.rbs.book_table(2, "Гость 2", booking_time)

        # Then: оба бронирования успешны
        self.assertTrue(success1)
        self.assertTrue(success2)

        # Then: оба бронирования активны
        active = self.rbs.get_active_bookings()
        self.assertEqual(len(active), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)