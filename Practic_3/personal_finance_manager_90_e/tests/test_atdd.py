# tests/test_atdd_finance.py
import unittest
from src.finance_manager import FinanceManager

class TestFinanceManagerATDD(unittest.TestCase):
    """
    ATDD-тесты для менеджера личных финансов.
    Моделируют сценарии проверки корректности финансового отчёта с точки зрения пользователя.
    Согласованы с "заказчиком" как приёмочные критерии.
    """

    def setUp(self):
        """Создаём новый менеджер перед каждым тестом."""
        self.fm = FinanceManager()

    # ============ Сценарий 1: Корректность итоговых сумм ============
    def test_financial_report_shows_correct_totals(self):
        """
        ATDD Сценарий 1 (Корректность отчёта):
        Given: Пользователь внёс доход 50000 и расходы 31000
        When: Генерирует финансовый отчёт
        Then: В отчёте total_income=50000, total_expense=31000, balance=19000
        """
        # Given
        self.fm.add_transaction(50000.0, "Зарплата", "income", "2025-04-01")
        self.fm.add_transaction(15000.0, "Аренда", "expense", "2025-04-02")
        self.fm.add_transaction(8000.0, "Продукты", "expense", "2025-04-03")
        self.fm.add_transaction(5000.0, "Развлечения", "expense", "2025-04-04")
        self.fm.add_transaction(3000.0, "Транспорт", "expense", "2025-04-05")

        # When
        report = self.fm.generate_report()

        # Then
        self.assertEqual(report["total_income"], 50000.0, "Сумма доходов некорректна")
        self.assertEqual(report["total_expense"], 31000.0, "Сумма расходов некорректна")
        self.assertEqual(report["balance"], 19000.0, "Баланс рассчитан неверно")

    # ============ Сценарий 2: Корректность анализа по категориям ============
    def test_financial_report_breaks_down_by_categories_correctly(self):
        """
        ATDD Сценарий 2 (Корректность отчёта):
        Given: Пользователь внёс доходы и расходы по разным категориям
        When: Генерирует финансовый отчёт
        Then: В отчёте income_by_category и expense_by_category содержат точные суммы по каждой категории
        """
        # Given
        self.fm.add_transaction(40000.0, "Зарплата", "income", "2025-04-01")
        self.fm.add_transaction(10000.0, "Фриланс", "income", "2025-04-02")
        self.fm.add_transaction(20000.0, "Аренда", "expense", "2025-04-03")
        self.fm.add_transaction(5000.0, "Продукты", "expense", "2025-04-04")
        self.fm.add_transaction(5000.0, "Продукты", "expense", "2025-04-05")  # вторая транзакция в ту же категорию

        # When
        report = self.fm.generate_report()

        # Then: Доходы по категориям
        income_by_cat = report["income_by_category"]
        self.assertEqual(income_by_cat["Зарплата"], 40000.0, "Сумма по категории 'Зарплата' неверна")
        self.assertEqual(income_by_cat["Фриланс"], 10000.0, "Сумма по категории 'Фриланс' неверна")

        # Then: Расходы по категориям
        expense_by_cat = report["expense_by_category"]
        self.assertEqual(expense_by_cat["Аренда"], 20000.0, "Сумма по категории 'Аренда' неверна")
        self.assertEqual(expense_by_cat["Продукты"], 10000.0, "Сумма по категории 'Продукты' неверна (должна быть суммой двух транзакций)")

    # ============ Сценарий 3: Корректность топ-3 расходов ============
    def test_financial_report_displays_top_3_expenses_correctly(self):
        """
        ATDD Сценарий 3 (Корректность отчёта):
        Given: Пользователь внёс расходы по 5 категориям
        When: Генерирует финансовый отчёт
        Then: В отчёте top_expenses содержит ровно 3 категории, отсортированные по убыванию суммы
        """
        # Given
        self.fm.add_transaction(30000.0, "Ипотека", "expense", "2025-04-01")
        self.fm.add_transaction(15000.0, "Автомобиль", "expense", "2025-04-02")
        self.fm.add_transaction(10000.0, "Образование", "expense", "2025-04-03")
        self.fm.add_transaction(8000.0, "Путешествия", "expense", "2025-04-04")
        self.fm.add_transaction(5000.0, "Подарки", "expense", "2025-04-05")

        # When
        report = self.fm.generate_report()

        # Then: Проверяем количество
        top_expenses = report["top_expenses"]
        self.assertEqual(len(top_expenses), 3, "Должно отображаться ровно 3 категории в топе")

        # Then: Проверяем порядок (должен быть по убыванию)
        categories = list(top_expenses.keys())
        amounts = list(top_expenses.values())

        self.assertEqual(categories[0], "Ипотека", "Первая категория в топе должна быть 'Ипотека'")
        self.assertEqual(categories[1], "Автомобиль", "Вторая категория в топе должна быть 'Автомобиль'")
        self.assertEqual(categories[2], "Образование", "Третья категория в топе должна быть 'Образование'")

        # Проверяем, что суммы идут в порядке убывания
        self.assertGreaterEqual(amounts[0], amounts[1], "Суммы не отсортированы по убыванию")
        self.assertGreaterEqual(amounts[1], amounts[2], "Суммы не отсортированы по убыванию")

    # ============ Сценарий 4: Корректность фильтрации по периоду ============
    def test_financial_report_filters_transactions_by_date_range_correctly(self):
        """
        ATDD Сценарий 4 (Корректность отчёта):
        Given: Пользователь внёс транзакции за разные даты
        When: Генерирует отчёт за период 2025-04-02 — 2025-04-04
        Then: В отчёт попадают только транзакции в этом периоде, итоги пересчитываются
        """
        # Given
        self.fm.add_transaction(10000.0, "Доход1", "income", "2025-04-01")  # вне периода
        self.fm.add_transaction(5000.0, "Расход1", "expense", "2025-04-02")  # в периоде
        self.fm.add_transaction(7000.0, "Доход2", "income", "2025-04-03")   # в периоде
        self.fm.add_transaction(3000.0, "Расход2", "expense", "2025-04-04")  # в периоде
        self.fm.add_transaction(2000.0, "Доход3", "income", "2025-04-05")   # вне периода

        # When
        report = self.fm.generate_report("2025-04-02", "2025-04-04")

        # Then: Проверяем итоги
        self.assertEqual(report["total_income"], 7000.0, "Доходы за период рассчитаны неверно")    # Только 7000.0 (Доход2)
        self.assertEqual(report["total_expense"], 8000.0, "Расходы за период рассчитаны неверно")   # 5000 + 3000
        self.assertEqual(report["balance"], -1000.0, "Баланс за период рассчитан неверно")          # 7000 - 8000 = -1000

        # Then: Проверяем количество транзакций
        self.assertEqual(report["transaction_count"], 3, "Количество транзакций в периоде неверно")

    # ============ Сценарий 5: Отчёт при отсутствии данных ============
    def test_financial_report_handles_empty_data_gracefully(self):
        """
        ATDD Сценарий 5 (Корректность отчёта):
        Given: Пользователь не внёс ни одной транзакции
        When: Генерирует финансовый отчёт
        Then: Отчёт содержит нулевые значения и пустые словари, не падает с ошибкой
        """
        # Given: ничего не добавлено
        # When
        report = self.fm.generate_report()

        # Then
        self.assertEqual(report["total_income"], 0.0, "Доходы должны быть 0.0")
        self.assertEqual(report["total_expense"], 0.0, "Расходы должны быть 0.0")
        self.assertEqual(report["balance"], 0.0, "Баланс должен быть 0.0")
        self.assertEqual(report["transaction_count"], 0, "Количество транзакций должно быть 0")
        self.assertEqual(report["income_by_category"], {}, "Словарь доходов по категориям должен быть пустым")
        self.assertEqual(report["expense_by_category"], {}, "Словарь расходов по категориям должен быть пустым")
        self.assertEqual(report["top_expenses"], {}, "Топ расходов должен быть пустым")


if __name__ == "__main__":
    unittest.main(verbosity=2)