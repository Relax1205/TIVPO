# tests/test_sdd_donation.py
import unittest
from src.donation_tracker import DonationTracker

class TestDonationTrackerSDD(unittest.TestCase):
    """
    SDD-тесты для трекера онлайн-пожертвований.
    На основе спецификации с примерами пожертвований и ожидаемыми отчётами.
    Спецификация находится в specs/donation_examples.md
    """

    def setUp(self):
        """Создаём новый трекер перед каждым тестом."""
        self.tracker = DonationTracker()

    # ============ Тест 1: Проверка общего отчёта (Таблица 2) ============
    def test_sdd_overall_report_specification(self):
        """
        SDD Тест 1: Проверка общего отчёта на основе Таблицы 2 спецификации.
        Добавляем все пожертвования из Таблицы 1 и сверяемся с ожиданиями.
        """
        # Given: все пожертвования из Таблицы 1
        donations_data = [
            ("Анна Петрова", 1500.0, "Помощь детям", "2025-04-01"),
            ("Иван Смирнов", 3000.0, "Экология", "2025-04-02"),
            ("Анна Петрова", 500.0, "Помощь детям", "2025-04-03"),
            ("Ольга Козлова", 2000.0, "Экология", "2025-04-04"),
            ("Иван Смирнов", 1000.0, "Помощь животным", "2025-04-05"),
        ]

        for donor, amount, cause, date in donations_data:
            self.tracker.log_donation(donor, amount, cause, date)

        # When: генерируем отчёт
        report = self.tracker.generate_report()

        # Then: сверяем с Таблицей 2
        self.assertAlmostEqual(report["total_amount"], 8000.0, places=2, msg="Неверная общая сумма")
        self.assertEqual(report["total_donations"], 5, msg="Неверное количество пожертвований")
        self.assertEqual(report["unique_donors"], 3, msg="Неверное количество уникальных доноров")
        self.assertEqual(report["top_donor"], "Иван Смирнов", msg="Неверный топ-донор")

    # ============ Тест 2: Проверка сводки по целям (Таблица 3) ============
    def test_sdd_causes_summary_specification(self):
        """
        SDD Тест 2: Проверка сводки по целям на основе Таблицы 3 спецификации.
        """
        # Given: все пожертвования
        donations_data = [
            ("Анна Петрова", 1500.0, "Помощь детям", "2025-04-01"),
            ("Иван Смирнов", 3000.0, "Экология", "2025-04-02"),
            ("Анна Петрова", 500.0, "Помощь детям", "2025-04-03"),
            ("Ольга Козлова", 2000.0, "Экология", "2025-04-04"),
            ("Иван Смирнов", 1000.0, "Помощь животным", "2025-04-05"),
        ]

        for donor, amount, cause, date in donations_data:
            self.tracker.log_donation(donor, amount, cause, date)

        # When: генерируем отчёт
        report = self.tracker.generate_report()
        causes_summary = report["causes_summary"]

        # Then: сверяем с Таблицей 3
        expected_causes = {
            "Помощь детям": 2000.0,
            "Экология": 5000.0,
            "Помощь животным": 1000.0
        }

        for cause, expected_amount in expected_causes.items():
            actual_amount = causes_summary.get(cause, 0.0)
            self.assertAlmostEqual(actual_amount, expected_amount, places=2,
                                   msg=f"Неверная сумма по цели '{cause}'")

        # Проверяем, что нет лишних целей
        self.assertEqual(len(causes_summary), len(expected_causes),
                         msg="В сводке по целям есть лишние или отсутствуют ожидаемые цели")

    # ============ Тест 3: Проверка истории донора (Таблица 4) ============
    def test_sdd_donor_history_specification(self):
        """
        SDD Тест 3: Проверка истории донора "Анна Петрова" на основе Таблицы 4 спецификации.
        """
        # Given: все пожертвования
        donations_data = [
            ("Анна Петрова", 1500.0, "Помощь детям", "2025-04-01"),
            ("Иван Смирнов", 3000.0, "Экология", "2025-04-02"),
            ("Анна Петрова", 500.0, "Помощь детям", "2025-04-03"),  # более новая
            ("Ольга Козлова", 2000.0, "Экология", "2025-04-04"),
            ("Иван Смирнов", 1000.0, "Помощь животным", "2025-04-05"),
        ]

        for donor, amount, cause, date in donations_data:
            self.tracker.log_donation(donor, amount, cause, date)

        # When: запрашиваем историю Анны Петровой
        anna_history = self.tracker.get_donations_by_donor("Анна Петрова")

        # Then: сверяем с Таблицей 4 (обратите внимание: записи отсортированы по дате, новые сверху!)
        self.assertEqual(len(anna_history), 2, msg="Неверное количество записей в истории Анны")

        # Первая запись — самая новая (2025-04-03)
        self.assertEqual(anna_history[0]["date"], "2025-04-03", msg="Первая запись должна быть самой новой")
        self.assertEqual(anna_history[0]["amount"], 500.0)
        self.assertEqual(anna_history[0]["cause"], "Помощь детям")

        # Вторая запись — более старая (2025-04-01)
        self.assertEqual(anna_history[1]["date"], "2025-04-01", msg="Вторая запись должна быть старой")
        self.assertEqual(anna_history[1]["amount"], 1500.0)
        self.assertEqual(anna_history[1]["cause"], "Помощь детям")

    # ============ Тест 4: Проверка граничных случаев (Таблица 5) ============
    def test_sdd_edge_cases_specification(self):
        """
        SDD Тест 4: Проверка граничных случаев на основе Таблицы 5 спецификации.
        """

        # Сценарий 1: Нет пожертвований
        empty_report = self.tracker.generate_report()
        self.assertEqual(empty_report["total_amount"], 0.0)
        self.assertEqual(empty_report["total_donations"], 0)
        self.assertEqual(empty_report["unique_donors"], 0)
        self.assertIsNone(empty_report["top_donor"])
        self.assertEqual(empty_report["causes_summary"], {})

        # Сценарий 2: Один донор, одна цель
        self.tracker.log_donation("Единственный Донор", 2500.0, "Единая Цель", "2025-04-06")
        single_report = self.tracker.generate_report()
        self.assertEqual(single_report["unique_donors"], 1)
        self.assertEqual(single_report["top_donor"], "Единственный Донор")
        self.assertEqual(single_report["causes_summary"], {"Единая Цель": 2500.0})

        # Сценарий 3: Два донора с одинаковой суммой
        # Создаём новый трекер для чистого теста
        tracker_equal = DonationTracker()
        tracker_equal.log_donation("Донор А", 1000.0, "Цель X", "2025-04-07")
        tracker_equal.log_donation("Донор Б", 1000.0, "Цель Y", "2025-04-08")
        equal_report = tracker_equal.generate_report()

        # Ожидаем, что top_donor — один из них (в нашей реализации — первый по алфавиту или порядку добавления)
        # Важно: тест не падает, если top_donor — любой из них, но мы проверяем, что он присутствует и корректен
        self.assertIn(equal_report["top_donor"], ["Донор А", "Донор Б"])
        self.assertEqual(equal_report["causes_summary"]["Цель X"], 1000.0)
        self.assertEqual(equal_report["causes_summary"]["Цель Y"], 1000.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)