# demo_finance.py
from src.finance_manager import FinanceManager

def main():
    # Создаём менеджер финансов
    fm = FinanceManager()

    # Добавляем доходы
    fm.add_transaction(50000.0, "Зарплата", "income", "2025-04-01")
    fm.add_transaction(10000.0, "Фриланс", "income", "2025-04-05")

    # Добавляем расходы
    fm.add_transaction(15000.0, "Аренда", "expense", "2025-04-02")
    fm.add_transaction(8000.0, "Продукты", "expense", "2025-04-03")
    fm.add_transaction(3000.0, "Транспорт", "expense", "2025-04-04")
    fm.add_transaction(5000.0, "Развлечения", "expense", "2025-04-06")

    # Получаем текущий баланс
    balance = fm.get_balance()
    print(f"💰 Текущий баланс: {balance} руб.")

    # Генерируем полный отчёт
    report = fm.generate_report()
    print(f"\n📊 Финансовый отчёт:")
    print(f"   Доходы: {report['total_income']} руб.")
    print(f"   Расходы: {report['total_expense']} руб.")
    print(f"   Баланс: {report['balance']} руб.")
    print(f"   Всего транзакций: {report['transaction_count']}")

    print(f"\n📈 Доходы по категориям:")
    for category, amount in report["income_by_category"].items():
        print(f"   - {category}: {amount} руб.")

    print(f"\n📉 Расходы по категориям:")
    for category, amount in report["expense_by_category"].items():
        print(f"   - {category}: {amount} руб.")

    print(f"\n🔝 Топ-3 категории расходов:")
    for category, amount in report["top_expenses"].items():
        print(f"   - {category}: {amount} руб.")


if __name__ == "__main__":
    main()