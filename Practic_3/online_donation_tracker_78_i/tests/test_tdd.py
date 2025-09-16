# tests/test_tdd_donation.py
import unittest
from src.donation_tracker import DonationTracker

class TestDonationTrackerTDD(unittest.TestCase):
    """
    TDD-тесты для трекера онлайн-пожертвований.
    Покрывают функции регистрации (логирования) пожертвований и генерации отчётов.
    """

    def setUp(self):
        """Создаём новый трекер перед каждым тестом."""
        self.tracker = DonationTracker()

    # ============ Этап 1: Тесты для РЕГИСТРАЦИИ (логирования) пожертвований ============
    def test_log_donation_records_correct_data(self):
        """TDD Шаг 1: Проверяем, что log_donation сохраняет пожертвование с правильными данными."""
        # Given: трекер пуст
        self.assertEqual(len(self.tracker.get_all_donations()), 0)

        # When: логируем пожертвование
        self.tracker.log_donation("Анна Петрова", 1500.0, "Помощь детям", "2025-04-01")

        # Then: появилось 1 пожертвование с корректными данными
        donations = self.tracker.get_all_donations()
        self.assertEqual(len(donations), 1)

        donation = donations[0]
        self.assertEqual(donation["donor_name"], "Анна Петрова")
        self.assertEqual(donation["amount"], 1500.0)
        self.assertEqual(donation["cause"], "Помощь детям")
        self.assertEqual(donation["date"], "2025-04-01")

    def test_log_donation_without_date_uses_today(self):
        """TDD Шаг 2: Если дата не указана — используется текущая дата."""
        # Given: ничего
        from datetime import datetime
        today_str = datetime.now().strftime("%Y-%m-%d")

        # When: логируем без указания даты
        self.tracker.log_donation("Иван Смирнов", 2000.0, "Экология")

        # Then: дата совпадает с сегодняшней
        donations = self.tracker.get_all_donations()
        self.assertEqual(len(donations), 1)
        self.assertEqual(donations[0]["date"], today_str)

    # ============ Этап 2: Тесты для ОТЧЁТОВ ============
    def test_generate_report_with_no_donations(self):
        """TDD Шаг 3: Отчёт при отсутствии пожертвований содержит нулевые значения."""
        # Given: трекер пуст
        # When: генерируем отчёт
        report = self.tracker.generate_report()

        # Then: все значения нулевые или None
        self.assertEqual(report["total_donations"], 0)
        self.assertEqual(report["total_amount"], 0.0)
        self.assertEqual(report["unique_donors"], 0)
        self.assertIsNone(report["top_donor"])
        self.assertEqual(report["causes_summary"], {})

    def test_generate_report_with_single_donation(self):
        """TDD Шаг 4: Отчёт корректно считается для одного пожертвования."""
        # Given: одно пожертвование
        self.tracker.log_donation("Ольга Козлова", 3000.0, "Помощь животным", "2025-04-02")

        # When: генерируем отчёт
        report = self.tracker.generate_report()

        # Then: статистика отражает одно пожертвование
        self.assertEqual(report["total_donations"], 1)
        self.assertEqual(report["total_amount"], 3000.0)
        self.assertEqual(report["unique_donors"], 1)
        self.assertEqual(report["top_donor"], "Ольга Козлова")
        self.assertEqual(report["causes_summary"], {"Помощь животным": 3000.0})

    def test_generate_report_with_multiple_donations(self):
        """TDD Шаг 5: Отчёт корректно агрегирует данные для нескольких пожертвований."""
        # Given: несколько пожертвований от разных доноров
        self.tracker.log_donation("Анна Петрова", 1500.0, "Помощь детям", "2025-04-01")
        self.tracker.log_donation("Иван Смирнов", 3000.0, "Экология", "2025-04-02")
        self.tracker.log_donation("Анна Петрова", 500.0, "Помощь детям", "2025-04-03")

        # When: генерируем отчёт
        report = self.tracker.generate_report()

        # Then: проверяем агрегацию
        self.assertEqual(report["total_donations"], 3)
        self.assertEqual(report["total_amount"], 5000.0)  # 1500 + 3000 + 500
        self.assertEqual(report["unique_donors"], 2)      # Анна + Иван

        # Проверяем топ-донора (Иван — 3000 > Анна — 2000)
        self.assertEqual(report["top_donor"], "Иван Смирнов")

        # Проверяем сводку по целям
        expected_causes = {
            "Помощь детям": 2000.0,  # 1500 + 500
            "Экология": 3000.0
        }
        self.assertEqual(report["causes_summary"], expected_causes)

    def test_get_all_donors_returns_unique_sorted_list(self):
        """TDD Шаг 6: get_all_donors возвращает уникальных доноров в отсортированном порядке."""
        # Given: несколько пожертвований
        self.tracker.log_donation("Иван Смирнов", 1000.0, "Цель 1")
        self.tracker.log_donation("Анна Петрова", 500.0, "Цель 2")
        self.tracker.log_donation("Иван Смирнов", 2000.0, "Цель 3")  # повторно

        # When: запрашиваем список доноров
        donors = self.tracker.get_all_donors()

        # Then: только уникальные имена, отсортированные
        self.assertEqual(len(donors), 2)
        self.assertEqual(donors[0], "Анна Петрова")  # по алфавиту
        self.assertEqual(donors[1], "Иван Смирнов")

    def test_get_donations_by_donor_returns_correct_list(self):
        """TDD Шаг 7: get_donations_by_donor возвращает только пожертвования указанного донора."""
        # Given: пожертвования от разных доноров
        self.tracker.log_donation("Анна Петрова", 1500.0, "Цель A")
        self.tracker.log_donation("Иван Смирнов", 3000.0, "Цель B")
        self.tracker.log_donation("Анна Петрова", 500.0, "Цель C")

        # When: запрашиваем пожертвования Анны
        anna_donations = self.tracker.get_donations_by_donor("Анна Петрова")

        # Then: возвращаются только её пожертвования (2 шт)
        self.assertEqual(len(anna_donations), 2)
        self.assertEqual(anna_donations[0]["amount"], 1500.0)
        self.assertEqual(anna_donations[1]["amount"], 500.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)