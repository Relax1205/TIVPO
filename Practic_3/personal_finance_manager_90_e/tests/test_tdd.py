# tests/test_tdd_finance.py
import unittest
from src.finance_manager import FinanceManager

class TestFinanceManagerTDD(unittest.TestCase):
    """
    TDD-тесты для менеджера личных финансов.
    Покрывают расчёт баланса и генерацию отчётов.
    """

    def setUp(self):
        """Создаём новый менеджер перед каждым тестом."""
        self.fm = FinanceManager()

    # ============ Этап 1: Тесты для РАСЧЁТА БАЛАНСА ============
    def test_balance_is_zero_with_no_transactions(self):
        """TDD Шаг 1: Баланс равен 0, если нет транзакций."""
        # Given: нет транзакций
        # When: запрашиваем баланс
        balance = self.fm.get_balance()

        # Then: баланс равен 0
        self.assertEqual(balance, 0.0)

    def test_balance_calculates_correctly_with_income_only(self):
        """TDD Шаг 2: Баланс корректно считается при наличии только доходов."""
        # Given: добавляем доходы
        self.fm.add_transaction(1000.0, "Зарплата", "income", "2025-04-01")
        self.fm.add_transaction(500.0, "Фриланс", "income", "2025-04-02")

        # When: запрашиваем баланс
        balance = self.fm.get_balance()

        # Then: баланс равен сумме доходов
        self.assertEqual(balance, 1500.0)

    def test_balance_calculates_correctly_with_expenses_only(self):
        """TDD Шаг 3: Баланс корректно считается при наличии только расходов (отрицательный баланс)."""
        # Given: добавляем расходы
        self.fm.add_transaction(300.0, "Продукты", "expense", "2025-04-01")
        self.fm.add_transaction(200.0, "Транспорт", "expense", "2025-04-02")

        # When: запрашиваем баланс
        balance = self.fm.get_balance()

        # Then: баланс равен отрицательной сумме расходов
        self.assertEqual(balance, -500.0)

    def test_balance_calculates_correctly_with_income_and_expenses(self):
        """TDD Шаг 4: Баланс корректно считается при наличии доходов и расходов."""
        # Given: добавляем доходы и расходы
        self.fm.add_transaction(2000.0, "Зарплата", "income", "2025-04-01")
        self.fm.add_transaction(800.0, "Продукты", "expense", "2025-04-02")
        self.fm.add_transaction(300.0, "Развлечения", "expense", "2025-04-03")

        # When: запрашиваем баланс
        balance = self.fm.get_balance()

        # Then: баланс = доходы - расходы
        self.assertEqual(balance, 2000.0 - 800.0 - 300.0)  # 900.0

    # ============ Этап 2: Тесты для ГЕНЕРАЦИИ ОТЧЁТОВ ============
    def test_generate_report_with_no_transactions(self):
        """TDD Шаг 5: Отчёт при отсутствии транзакций содержит нулевые значения."""
        # Given: нет транзакций
        # When: генерируем отчёт
        report = self.fm.generate_report()

        # Then: все значения нулевые
        self.assertEqual(report["total_income"], 0.0)
        self.assertEqual(report["total_expense"], 0.0)
        self.assertEqual(report["balance"], 0.0)
        self.assertEqual(report["transaction_count"], 0)
        self.assertEqual(report["income_by_category"], {})
        self.assertEqual(report["expense_by_category"], {})
        self.assertEqual(report["top_expenses"], {})

    def test_generate_report_with_income_and_expenses(self):
        """TDD Шаг 6: Отчёт корректно агрегирует данные по категориям и рассчитывает баланс."""
        # Given: добавляем транзакции
        self.fm.add_transaction(3000.0, "Зарплата", "income", "2025-04-01")
        self.fm.add_transaction(1000.0, "Бонус", "income", "2025-04-02")
        self.fm.add_transaction(1500.0, "Аренда", "expense", "2025-04-03")
        self.fm.add_transaction(800.0, "Продукты", "expense", "2025-04-04")
        self.fm.add_transaction(300.0, "Транспорт", "expense", "2025-04-05")

        # When: генерируем отчёт
        report = self.fm.generate_report()

        # Then: проверяем агрегацию
        self.assertEqual(report["total_income"], 4000.0)  # 3000 + 1000
        self.assertEqual(report["total_expense"], 2600.0) # 1500 + 800 + 300
        self.assertEqual(report["balance"], 1400.0)       # 4000 - 2600

        # Then: проверяем доходы по категориям
        self.assertEqual(report["income_by_category"]["Зарплата"], 3000.0)
        self.assertEqual(report["income_by_category"]["Бонус"], 1000.0)

        # Then: проверяем расходы по категориям
        self.assertEqual(report["expense_by_category"]["Аренда"], 1500.0)
        self.assertEqual(report["expense_by_category"]["Продукты"], 800.0)
        self.assertEqual(report["expense_by_category"]["Транспорт"], 300.0)

        # Then: проверяем топ-3 расходов (должны быть все, так как их 3)
        top_expenses = report["top_expenses"]
        self.assertEqual(len(top_expenses), 3)
        self.assertEqual(list(top_expenses.keys())[0], "Аренда")      # Самый большой расход
        self.assertEqual(list(top_expenses.keys())[1], "Продукты")    # Второй по величине
        self.assertEqual(list(top_expenses.keys())[2], "Транспорт")   # Третий

    def test_generate_report_with_date_filtering(self):
        """TDD Шаг 7: Отчёт корректно фильтрует транзакции по дате."""
        # Given: добавляем транзакции за разные даты
        self.fm.add_transaction(1000.0, "Доход1", "income", "2025-04-01")
        self.fm.add_transaction(500.0, "Расход1", "expense", "2025-04-02")
        self.fm.add_transaction(2000.0, "Доход2", "income", "2025-04-10")
        self.fm.add_transaction(800.0, "Расход2", "expense", "2025-04-11")

        # When: генерируем отчёт за период 2025-04-01 — 2025-04-05
        report = self.fm.generate_report("2025-04-01", "2025-04-05")

        # Then: учитываются только первые две транзакции
        self.assertEqual(report["total_income"], 1000.0)
        self.assertEqual(report["total_expense"], 500.0)
        self.assertEqual(report["balance"], 500.0)
        self.assertEqual(report["transaction_count"], 2)

    # ============ Этап 3: Тесты для ОБРАБОТКИ ОШИБОК ============
    def test_add_transaction_with_negative_amount_raises_error(self):
        """TDD Шаг 8: Попытка добавить транзакцию с отрицательной суммой вызывает ValueError."""
        with self.assertRaises(ValueError) as context:
            self.fm.add_transaction(-100.0, "Продукты", "expense", "2025-04-01")
        self.assertIn("должна быть положительной", str(context.exception))

    def test_add_transaction_with_invalid_type_raises_error(self):
        """TDD Шаг 9: Попытка добавить транзакцию с неверным типом вызывает ValueError."""
        with self.assertRaises(ValueError) as context:
            self.fm.add_transaction(100.0, "Продукты", "invalid_type", "2025-04-01")
        self.assertIn("должен быть 'income' или 'expense'", str(context.exception))


if __name__ == "__main__":
    unittest.main(verbosity=2)