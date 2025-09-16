# src/restaurant_booking.py
from datetime import datetime
from typing import List, Dict, Optional

class RestaurantBookingSystem:
    """
    Система бронирования столиков в ресторане.
    Позволяет бронировать, отменять и просматривать бронирования.
    """

    def __init__(self):
        self.bookings: List[Dict[str, any]] = []  # Список всех бронирований

    def book_table(self, table_number: int, customer_name: str, booking_time: str) -> bool:
        """
        Бронирует столик на указанное время.
        
        :param table_number: Номер столика
        :param customer_name: Имя клиента
        :param booking_time: Время бронирования в формате 'YYYY-MM-DD HH:MM'
        :return: True, если бронирование успешно; False, если столик уже занят в это время
        :raises ValueError: если параметры пустые или время в прошлом
        """
        if not table_number or not customer_name or not booking_time:
            raise ValueError("Все поля должны быть заполнены")

        # Проверяем, не в прошлом ли время
        booking_dt = datetime.strptime(booking_time, "%Y-%m-%d %H:%M")
        if booking_dt < datetime.now():
            raise ValueError("Нельзя забронировать столик на прошедшее время")

        # Проверяем, не занят ли столик в это время
        for booking in self.bookings:
            if booking["table_number"] == table_number and booking["booking_time"] == booking_time:
                return False  # Столик уже забронирован

        # Создаём новое бронирование
        new_booking = {
            "table_number": table_number,
            "customer_name": customer_name,
            "booking_time": booking_time,
            "status": "confirmed"
        }
        self.bookings.append(new_booking)
        return True

    def cancel_booking(self, table_number: int, booking_time: str) -> bool:
        """
        Отменяет бронирование столика на указанное время.
        
        :param table_number: Номер столика
        :param booking_time: Время бронирования
        :return: True, если отмена успешна; False, если бронирование не найдено
        """
        for booking in self.bookings:
            if booking["table_number"] == table_number and booking["booking_time"] == booking_time:
                booking["status"] = "cancelled"
                return True
        return False

    def get_all_bookings(self) -> List[Dict]:
        """
        Возвращает список всех бронирований (активных и отменённых).
        
        :return: Список бронирований
        """
        return self.bookings.copy()

    def get_active_bookings(self) -> List[Dict]:
        """
        Возвращает список только активных (не отменённых) бронирований.
        
        :return: Список активных бронирований
        """
        return [b for b in self.bookings if b["status"] == "confirmed"]

    def is_table_available(self, table_number: int, booking_time: str) -> bool:
        """
        Проверяет, доступен ли столик на указанное время.
        
        :param table_number: Номер столика
        :param booking_time: Время бронирования
        :return: True, если столик свободен; False, если занят
        """
        for booking in self.bookings:
            if booking["table_number"] == table_number and booking["booking_time"] == booking_time and booking["status"] == "confirmed":
                return False
        return True