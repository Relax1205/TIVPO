# src/donation_tracker.py
from datetime import datetime
from typing import List, Dict, Any, Optional

class DonationTracker:
    """
    Трекер онлайн-пожертвований.
    Позволяет логировать пожертвования, просматривать доноров и генерировать отчёты.
    """

    def __init__(self):
        self.donations: List[Dict[str, Any]] = []  # Список всех пожертвований

    def log_donation(self, donor_name: str, amount: float, cause: str, date_str: Optional[str] = None) -> None:
        """
        Логирует новое пожертвование.
        
        :param donor_name: Имя донора
        :param amount: Сумма пожертвования
        :param cause: Цель пожертвования (например, "Помощь детям", "Экология")
        :param date_str: Дата в формате 'YYYY-MM-DD'. Если не указана — используется текущая дата.
        """
        if date_str is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        donation = {
            "donor_name": donor_name,
            "amount": amount,
            "cause": cause,
            "date": date_str
        }
        self.donations.append(donation)

    def get_all_donors(self) -> List[str]:
        """
        Возвращает список уникальных доноров.
        
        :return: Список имён доноров без дубликатов
        """
        donors = set()
        for donation in self.donations:
            donors.add(donation["donor_name"])
        return sorted(list(donors))  # Возвращаем отсортированный список для детерминизма

    def generate_report(self) -> Dict[str, Any]:
        """
        Генерирует общий отчёт по всем пожертвованиям.
        
        :return: Словарь с ключевой статистикой
        """
        if not self.donations:
            return {
                "total_donations": 0,
                "total_amount": 0.0,
                "unique_donors": 0,
                "top_donor": None,
                "causes_summary": {}
            }

        total_amount = sum(d["amount"] for d in self.donations)
        total_donations = len(self.donations)
        unique_donors = len(self.get_all_donors())

        # Находим топ-донора (по общей сумме)
        donor_totals = {}
        for donation in self.donations:
            name = donation["donor_name"]
            donor_totals[name] = donor_totals.get(name, 0) + donation["amount"]

        top_donor = max(donor_totals, key=donor_totals.get)

        # Сводка по целям
        causes_summary = {}
        for donation in self.donations:
            cause = donation["cause"]
            causes_summary[cause] = causes_summary.get(cause, 0) + donation["amount"]

        return {
            "total_donations": total_donations,
            "total_amount": round(total_amount, 2),
            "unique_donors": unique_donors,
            "top_donor": top_donor,
            "causes_summary": causes_summary
        }

    def get_donations_by_donor(self, donor_name: str) -> List[Dict]:
        """
        Возвращает все пожертвования конкретного донора, отсортированные по дате (от новых к старым).
        
        :param donor_name: Имя донора
        :return: Список пожертвований, отсортированный по убыванию даты
        """
        donations = [d for d in self.donations if d["donor_name"] == donor_name]
        # Сортируем по дате в обратном порядке (новые сверху)
        return sorted(donations, key=lambda x: x["date"], reverse=True)

    def get_all_donations(self) -> List[Dict]:
        """
        Возвращает полный список всех пожертвований (для отладки и тестов).
        """
        return self.donations.copy()