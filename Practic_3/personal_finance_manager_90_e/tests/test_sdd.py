# tests/test_sdd_finance.py
import unittest
from src.finance_manager import FinanceManager

class TestFinanceManagerSDD(unittest.TestCase):
    """
    SDD-тесты для менеджера личных финансов.
    На основе спецификации с примерами доходов, расходов и итоговых расчётов.
    Спецификация находится в specs/finance_specifications.md
    """

    def setUp(self):
        """Создаём новый менеджер перед каждым тестом."""
        self.fm = FinanceManager()

    # ============ Тест 1: Проверка пошагового добавления транзакций (Таблица 1) ============
    def test_sdd_specification_table1_step_by_step_transactions(self):
        """
        SDD Тест 1: Пошаговая проверка отчёта после каждой транзакции (Таблица 1).
        """
        transactions = [
            ("2025-04-01", "income", "Зарплата", 50000.0),
            ("2025-04-02", "expense", "Аренда", 15000.0),
            ("2025-04-03", "expense", "Продукты", 8000.0),
            ("2025-04-04", "income", "Фриланс", 10000.0),
            ("2025-04-05", "expense", "Развлечения", 5000.0),
        ]

        expected_results = [
            (50000.0, 0.0, 50000.0, {}),  # После шага 1
            (50000.0, 15000.0, 35000.0, {"Аренда": 15000.0}),  # После шага 2
            (50000.0, 23000.0, 27000.0, {"Аренда": 15000.0, "Продукты": 8000.0}),  # После шага 3
            (60000.0, 23000.0, 37000.0, {"Аренда": 15000.0, "Продукты": 8000.0}),  # После шага 4
            (60000.0, 28000.0, 32000.0, {"Аренда": 15000.0, "Продукты": 8000.0, "Развлечения": 5000.0}),  # После шага 5
        ]

        for i, (date, t_type, category, amount) in enumerate(transactions):
            # When: добавляем транзакцию
            self.fm.add_transaction(amount, category, t_type, date)

            # When: генерируем отчёт
            report = self.fm.generate_report()

            # Then: сверяем с ожиданиями из Таблицы 1
            exp_income, exp_expense, exp_balance, exp_top = expected_results[i]

            self.assertAlmostEqual(report["total_income"], exp_income, places=2,
                                   msg=f"Шаг {i+1}: Неверная сумма доходов")
            self.assertAlmostEqual(report["total_expense"], exp_expense, places=2,
                                   msg=f"Шаг {i+1}: Неверная сумма расходов")
            self.assertAlmostEqual(report["balance"], exp_balance, places=2,
                                   msg=f"Шаг {i+1}: Неверный баланс")

            # Проверяем top_expenses
            top_expenses = report["top_expenses"]
            self.assertEqual(len(top_expenses), len(exp_top),
                             msg=f"Шаг {i+1}: Неверное количество категорий в top_expenses")
            for category_name, expected_amount in exp_top.items():
                self.assertIn(category_name, top_expenses,
                              msg=f"Шаг {i+1}: Категория '{category_name}' отсутствует в top_expenses")
                self.assertAlmostEqual(top_expenses[category_name], expected_amount, places=2,
                                       msg=f"Шаг {i+1}: Неверная сумма для категории '{category_name}'")

    # ============ Тест 2: Проверка отчётов за период (Таблица 2) ============
    def test_sdd_specification_table2_period_reports(self):
        """
        SDD Тест 2: Проверка отчётов за указанные периоды (Таблица 2).
        """
        # Given: добавляем все транзакции
        transactions = [
            ("2025-04-01", "income", "Зарплата", 50000.0),
            ("2025-04-02", "expense", "Аренда", 15000.0),
            ("2025-04-03", "expense", "Продукты", 8000.0),
            ("2025-04-04", "income", "Фриланс", 10000.0),
            ("2025-04-05", "expense", "Развлечения", 5000.0),
        ]

        for date, t_type, category, amount in transactions:
            self.fm.add_transaction(amount, category, t_type, date)

        # Период 1: 2025-04-02 — 2025-04-04
        report1 = self.fm.generate_report("2025-04-02", "2025-04-04")
        self.assertAlmostEqual(report1["total_income"], 10000.0, places=2)
        self.assertAlmostEqual(report1["total_expense"], 23000.0, places=2)
        self.assertAlmostEqual(report1["balance"], -13000.0, places=2)

        # Период 2: 2025-04-01 — 2025-04-03
        report2 = self.fm.generate_report("2025-04-01", "2025-04-03")
        self.assertAlmostEqual(report2["total_income"], 50000.0, places=2)
        self.assertAlmostEqual(report2["total_expense"], 23000.0, places=2)
        self.assertAlmostEqual(report2["balance"], 27000.0, places=2)

        # Период 3: 2025-04-05 — 2025-04-05
        report3 = self.fm.generate_report("2025-04-05", "2025-04-05")
        self.assertAlmostEqual(report3["total_income"], 0.0, places=2)
        self.assertAlmostEqual(report3["total_expense"], 5000.0, places=2)
        self.assertAlmostEqual(report3["balance"], -5000.0, places=2)

    # ============ Тест 3: Проверка граничных случаев (Таблица 3) ============
    def test_sdd_specification_table3_edge_cases(self):
        """
        SDD Тест 3: Проверка граничных случаев (Таблица 3).
        """
        # Сценарий 1: Пустой список
        empty_report = self.fm.generate_report()
        self.assertEqual(empty_report["total_income"], 0.0)
        self.assertEqual(empty_report["total_expense"], 0.0)
        self.assertEqual(empty_report["balance"], 0.0)
        self.assertEqual(empty_report["top_expenses"], {})

        # Сценарий 2: Одна транзакция дохода
        fm_income = FinanceManager()
        fm_income.add_transaction(10000.0, "Подарок", "income", "2025-04-06")
        report_income = fm_income.generate_report()
        self.assertEqual(report_income["total_income"], 10000.0)
        self.assertEqual(report_income["total_expense"], 0.0)
        self.assertEqual(report_income["balance"], 10000.0)

        # Сценарий 3: Одна транзакция расхода
        fm_expense = FinanceManager()
        fm_expense.add_transaction(5000.0, "Лекарства", "expense", "2025-04-07")
        report_expense = fm_expense.generate_report()
        self.assertEqual(report_expense["total_income"], 0.0)
        self.assertEqual(report_expense["total_expense"], 5000.0)
        self.assertEqual(report_expense["balance"], -5000.0)

        # Сценарий 4: Несколько расходов в одной категории
        fm_same_category = FinanceManager()
        fm_same_category.add_transaction(3000.0, "Продукты", "expense", "2025-04-08")
        fm_same_category.add_transaction(2000.0, "Продукты", "expense", "2025-04-09")
        report_same = fm_same_category.generate_report()
        self.assertEqual(report_same["expense_by_category"]["Продукты"], 5000.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)