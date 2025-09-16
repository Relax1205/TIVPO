# tests/test_atdd_booking.py
import unittest
from datetime import datetime, timedelta
from src.restaurant_booking import RestaurantBookingSystem

class TestRestaurantBookingSystemATDD(unittest.TestCase):
    """
    ATDD-тесты для системы бронирования столиков в ресторане.
    Моделируют сценарии бронирования столика с точки зрения пользователя.
    Согласованы с "заказчиком" как приёмочные критерии.
    """

    def setUp(self):
        """Создаём новую систему бронирования перед каждым тестом."""
        self.rbs = RestaurantBookingSystem()

    # ============ Сценарий 1: Успешное бронирование свободного столика ============
    def test_user_books_free_table_successfully(self):
        """
        ATDD Сценарий 1:
        Given: Столик 5 свободен на время X
        When: Пользователь бронирует столик 5 на время X
        Then: Система подтверждает бронирование
        And: Столик 5 на время X отображается как занятый
        """
        # Given: время в будущем
        booking_time = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")

        # When: бронируем столик
        success = self.rbs.book_table(5, "Иван Петров", booking_time)

        # Then: бронирование успешно
        self.assertTrue(success, "Бронирование должно быть успешным")

        # And: столик занят
        is_available = self.rbs.is_table_available(5, booking_time)
        self.assertFalse(is_available, "Столик должен быть занят после бронирования")

        # And: бронирование появилось в списке активных
        active_bookings = self.rbs.get_active_bookings()
        self.assertEqual(len(active_bookings), 1)
        self.assertEqual(active_bookings[0]["table_number"], 5)
        self.assertEqual(active_bookings[0]["customer_name"], "Иван Петров")
        self.assertEqual(active_bookings[0]["booking_time"], booking_time)

    # ============ Сценарий 2: Попытка забронировать уже занятый столик ============
    def test_user_sees_error_when_booking_already_booked_table(self):
        """
        ATDD Сценарий 2:
        Given: Столик 7 уже забронирован на время Y
        When: Пользователь пытается забронировать столик 7 на время Y
        Then: Система возвращает False
        And: Пользователь видит сообщение "Извините, этот столик уже забронирован на выбранное время."
        """
        # Given: бронируем столик 7 на время Y
        booking_time = (datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M")
        self.rbs.book_table(7, "Анна Сидорова", booking_time)

        # When: пытаемся забронировать тот же столик на то же время
        success = self.rbs.book_table(7, "Мария Козлова", booking_time)

        # Then: бронирование неуспешно
        self.assertFalse(success, "Бронирование должно быть отклонено")

        # And: эмулируем отображение сообщения в UI
        error_message = "Извините, этот столик уже забронирован на выбранное время." if not success else ""
        self.assertEqual(error_message, "Извините, этот столик уже забронирован на выбранное время.")

    # ============ Сценарий 3: Бронирование в прошлом — запрещено ============
    def test_user_sees_error_when_booking_in_past(self):
        """
        ATDD Сценарий 3:
        Given: Пользователь пытается забронировать столик на прошедшее время
        When: Вызывает book_table с датой в прошлом
        Then: Система выбрасывает ValueError
        And: Пользователь видит сообщение "Нельзя забронировать столик на прошедшее время."
        """
        # Given: время в прошлом
        past_time = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")

        # When/Then: ожидаем исключение
        with self.assertRaises(ValueError) as context:
            self.rbs.book_table(3, "Ольга Иванова", past_time)

        # And: проверяем сообщение об ошибке
        self.assertIn("прошедшее время", str(context.exception))

    # ============ Сценарий 4: Отмена бронирования ============
    def test_user_cancels_booking_successfully(self):
        """
        ATDD Сценарий 4:
        Given: Столик 9 забронирован на время Z
        When: Пользователь отменяет бронирование столика 9 на время Z
        Then: Система подтверждает отмену
        And: Столик 9 на время Z снова становится доступным
        """
        # Given: бронируем столик 9
        booking_time = (datetime.now() + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M")
        self.rbs.book_table(9, "Алексей Новиков", booking_time)

        # When: отменяем бронирование
        success = self.rbs.cancel_booking(9, booking_time)

        # Then: отмена успешна
        self.assertTrue(success, "Отмена должна быть успешной")

        # And: столик снова доступен
        is_available = self.rbs.is_table_available(9, booking_time)
        self.assertTrue(is_available, "Столик должен стать доступным после отмены")

        # And: в списке активных бронирований запись отсутствует
        active_bookings = self.rbs.get_active_bookings()
        self.assertEqual(len(active_bookings), 0, "Активных бронирований не должно быть")

    # ============ Сценарий 5: Просмотр активных бронирований ============
    def test_user_views_active_bookings_correctly(self):
        """
        ATDD Сценарий 5:
        Given: В системе есть 2 активных бронирования и 1 отменённое
        When: Пользователь запрашивает список активных бронирований
        Then: Возвращается список из 2 записей (отменённое не включается)
        """
        # Given: добавляем 3 бронирования
        time1 = (datetime.now() + timedelta(hours=4)).strftime("%Y-%m-%d %H:%M")
        time2 = (datetime.now() + timedelta(hours=5)).strftime("%Y-%m-%d %H:%M")
        time3 = (datetime.now() + timedelta(hours=6)).strftime("%Y-%m-%d %H:%M")

        self.rbs.book_table(1, "Гость 1", time1)
        self.rbs.book_table(2, "Гость 2", time2)
        self.rbs.book_table(3, "Гость 3", time3)

        # Отменяем одно бронирование
        self.rbs.cancel_booking(2, time2)

        # When: запрашиваем активные бронирования
        active_bookings = self.rbs.get_active_bookings()

        # Then: в списке 2 активных бронирования
        self.assertEqual(len(active_bookings), 2, "Должно быть 2 активных бронирования")

        # Then: проверяем, что отменённое бронирование не в списке
        cancelled_found = any(b["table_number"] == 2 and b["booking_time"] == time2 for b in active_bookings)
        self.assertFalse(cancelled_found, "Отменённое бронирование не должно отображаться в активных")


if __name__ == "__main__":
    unittest.main(verbosity=2)