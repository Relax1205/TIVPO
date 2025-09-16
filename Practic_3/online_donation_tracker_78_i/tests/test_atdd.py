# tests/test_atdd_donation.py
import unittest
from src.donation_tracker import DonationTracker

class TestDonationTrackerATDD(unittest.TestCase):
    """
    ATDD-тесты для трекера онлайн-пожертвований.
    Моделируют сценарии отображения истории доноров с точки зрения пользователя.
    Согласованы с "заказчиком" как приёмочные критерии.
    """

    def setUp(self):
        """Создаём новый трекер перед каждым тестом."""
        self.tracker = DonationTracker()

        # Предустановленные данные для всех тестов (фикстуры)
        self.tracker.log_donation("Анна Петрова", 1500.0, "Помощь детям", "2025-04-01")
        self.tracker.log_donation("Иван Смирнов", 3000.0, "Экология", "2025-04-02")
        self.tracker.log_donation("Анна Петрова", 500.0, "Помощь детям", "2025-04-03")
        self.tracker.log_donation("Ольга Козлова", 2000.0, "Экология", "2025-04-04")
        self.tracker.log_donation("Иван Смирнов", 1000.0, "Помощь животным", "2025-04-05")

    # ============ Сценарий 1: Просмотр полной истории пожертвований донора ============
    def test_user_views_full_donation_history_for_donor(self):
        """
        ATDD Сценарий 1:
        Given: Донор "Анна Петрова" имеет 2 пожертвования
        When: Пользователь запрашивает историю пожертвований Анны Петровой
        Then: Видит список из 2 записей с корректными суммами, датами и целями
            (в порядке от новых к старым)
        """
        # When
        anna_history = self.tracker.get_donations_by_donor("Анна Петрова")

        # Then: Проверяем количество записей
        self.assertEqual(len(anna_history), 2)

        # Then: Проверяем содержание первой записи (самая НОВАЯ — 2025-04-03)
        self.assertEqual(anna_history[0]["amount"], 500.0)
        self.assertEqual(anna_history[0]["cause"], "Помощь детям")
        self.assertEqual(anna_history[0]["date"], "2025-04-03")

        # Then: Проверяем содержание второй записи (самая СТАРАЯ — 2025-04-01)
        self.assertEqual(anna_history[1]["amount"], 1500.0)
        self.assertEqual(anna_history[1]["cause"], "Помощь детям")
        self.assertEqual(anna_history[1]["date"], "2025-04-01")

    # ============ Сценарий 2: Фильтрация истории по цели пожертвования ============
    def test_user_filters_donation_history_by_cause(self):
        """
        ATDD Сценарий 2:
        Given: Донор "Иван Смирнов" имеет пожертвования на разные цели
        When: Пользователь фильтрует историю Ивана по цели "Экология"
        Then: Видит только одно пожертвование на "Экология"
        """
        # When: получаем всю историю Ивана
        ivan_history = self.tracker.get_donations_by_donor("Иван Смирнов")

        # When: фильтруем по цели "Экология"
        ecology_donations = [d for d in ivan_history if d["cause"] == "Экология"]

        # Then: только одно пожертвование на "Экология"
        self.assertEqual(len(ecology_donations), 1)
        self.assertEqual(ecology_donations[0]["amount"], 3000.0)
        self.assertEqual(ecology_donations[0]["date"], "2025-04-02")

    # ============ Сценарий 3: Отображение сообщения при отсутствии пожертвований ============
    def test_user_sees_message_when_donor_has_no_donations(self):
        """
        ATDD Сценарий 3:
        Given: Донор "Сергей Иванов" не существует в системе (или у него нет пожертвований)
        When: Пользователь запрашивает историю пожертвований Сергея Иванова
        Then: Видит сообщение "У этого донора пока нет пожертвований."
        """
        # When
        sergey_history = self.tracker.get_donations_by_donor("Сергей Иванов")

        # Then: возвращается пустой список
        self.assertEqual(len(sergey_history), 0)

        # Then: в UI должно отображаться сообщение (эмулируем логику отображения)
        display_message = "У этого донора пока нет пожертвований." if len(sergey_history) == 0 else ""
        self.assertEqual(display_message, "У этого донора пока нет пожертвований.")

    # ============ Сценарий 4: Сортировка истории по дате (от новых к старым) ============
    def test_donation_history_is_sorted_by_date_descending(self):
        """
        ATDD Сценарий 4:
        Given: Донор "Анна Петрова" имеет пожертвования от 2025-04-01 и 2025-04-03
        When: Пользователь запрашивает историю пожертвований Анны
        Then: Записи отображаются в порядке от самой новой к самой старой (2025-04-03, затем 2025-04-01)
        """
        # When
        anna_history = self.tracker.get_donations_by_donor("Анна Петрова")

        # Then: сортируем вручную по дате (от новых к старым) для сравнения
        sorted_history = sorted(anna_history, key=lambda x: x["date"], reverse=True)

        # Then: проверяем, что история уже в правильном порядке (новые сверху)
        self.assertEqual(anna_history, sorted_history)
        # Первая запись — самая новая
        self.assertEqual(anna_history[0]["date"], "2025-04-03")
        self.assertEqual(anna_history[1]["date"], "2025-04-01")


if __name__ == "__main__":
    unittest.main(verbosity=2)