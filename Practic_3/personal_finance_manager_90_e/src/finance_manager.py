# src/finance_manager.py
from datetime import datetime
from typing import List, Dict, Any, Optional

class FinanceManager:
    """
    Менеджер личных финансов.
    Позволяет учитывать доходы и расходы, генерировать отчёты и анализировать финансы.
    """

    def __init__(self):
        self.transactions: List[Dict[str, Any]] = []  # Список всех транзакций

    def add_transaction(self, amount: float, category: str, transaction_type: str, date_str: Optional[str] = None) -> None:
        """
        Добавляет новую транзакцию (доход или расход).
        
        :param amount: Сумма транзакции (всегда положительная)
        :param category: Категория (например, "Зарплата", "Продукты", "Транспорт")
        :param transaction_type: Тип транзакции ("income" или "expense")
        :param date_str: Дата в формате 'YYYY-MM-DD'. Если не указана — используется текущая дата.
        """
        if amount <= 0:
            raise ValueError("Сумма транзакции должна быть положительной")
        if transaction_type not in ["income", "expense"]:
            raise ValueError("Тип транзакции должен быть 'income' или 'expense'")

        if date_str is None:
            date_str = datetime.now().strftime("%Y-%m-%d")

        transaction = {
            "amount": amount,
            "category": category,
            "type": transaction_type,
            "date": date_str
        }
        self.transactions.append(transaction)

    def get_balance(self) -> float:
        """
        Рассчитывает текущий баланс (доходы минус расходы).
        
        :return: Баланс (может быть отрицательным)
        """
        total_income = sum(t["amount"] for t in self.transactions if t["type"] == "income")
        total_expense = sum(t["amount"] for t in self.transactions if t["type"] == "expense")
        return round(total_income - total_expense, 2)

    def generate_report(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Генерирует финансовый отчёт за указанный период.
        
        :param start_date: Начальная дата в формате 'YYYY-MM-DD'
        :param end_date: Конечная дата в формате 'YYYY-MM-DD'
        :return: Словарь с отчётом
        """
        # Фильтруем транзакции по дате, если указаны границы
        filtered_transactions = self.transactions
        if start_date or end_date:
            filtered_transactions = [
                t for t in self.transactions
                if self._is_in_date_range(t["date"], start_date, end_date)
            ]

        total_income = sum(t["amount"] for t in filtered_transactions if t["type"] == "income")
        total_expense = sum(t["amount"] for t in filtered_transactions if t["type"] == "expense")
        balance = total_income - total_expense

        # Анализ по категориям
        income_by_category = {}
        expense_by_category = {}
        for t in filtered_transactions:
            category = t["category"]
            if t["type"] == "income":
                income_by_category[category] = income_by_category.get(category, 0) + t["amount"]
            else:
                expense_by_category[category] = expense_by_category.get(category, 0) + t["amount"]

        # Топ-3 категории расходов (если есть)
        top_expenses = sorted(expense_by_category.items(), key=lambda x: x[1], reverse=True)[:3]
        top_expenses = dict(top_expenses)

        return {
            "total_income": round(total_income, 2),
            "total_expense": round(total_expense, 2),
            "balance": round(balance, 2),
            "income_by_category": income_by_category,
            "expense_by_category": expense_by_category,
            "top_expenses": top_expenses,
            "transaction_count": len(filtered_transactions)
        }

    def _is_in_date_range(self, transaction_date: str, start_date: Optional[str], end_date: Optional[str]) -> bool:
        """
        Проверяет, попадает ли дата транзакции в указанный диапазон.
        """
        from datetime import datetime
        t_date = datetime.strptime(transaction_date, "%Y-%m-%d")

        if start_date:
            s_date = datetime.strptime(start_date, "%Y-%m-%d")
            if t_date < s_date:
                return False

        if end_date:
            e_date = datetime.strptime(end_date, "%Y-%m-%d")
            if t_date > e_date:
                return False

        return True

    def get_all_transactions(self) -> List[Dict]:
        """
        Возвращает полный список транзакций (для отладки и тестов).
        """
        return self.transactions.copy()