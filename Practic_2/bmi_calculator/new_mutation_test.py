# mutation_test.py

import importlib
import inspect
import sys
from io import StringIO

# Перехватываем оригинальный модуль
import bmi_calculator

# Копируем оригинальный исходный код функции для мутаций
def get_function_source(func):
    return inspect.getsource(func)

# Мутант 1: Увеличиваем коэффициент на 10% (ошибка в сторону увеличения)
def convert_ft_in_to_m_mutant1(feet, inches):
    total_inches = feet * 12 + inches
    return round(total_inches * 0.284, 2)  # 0.254 → 0.284 (ошибка)

# Мутант 2: Уменьшаем коэффициент (ошибка округления)
def convert_ft_in_to_m_mutant2(feet, inches):
    total_inches = feet * 12 + inches
    return round(total_inches * 0.234, 2)  # 0.254 → 0.234

# Мутант 3: Забываем про дюймы
def convert_ft_in_to_m_mutant3(feet, inches):
    total_inches = feet * 12  # ❌ забыли + inches
    return round(total_inches * 0.0254, 2)

# Мутант 4: Неправильное преобразование — используем только feet
def convert_ft_in_to_m_mutant4(feet, inches):
    return round(feet * 0.3048 + inches * 0.0254, 2)  # Но без суммы в дюймах

# Мутант 5: Возвращаем метры без округления
def convert_ft_in_to_m_mutant5(feet, inches):
    total_inches = feet * 12 + inches
    return total_inches * 0.0254  # ❌ нет округления

# Мутант 6: Ошибка в переводе футов (не 12 дюймов)
def convert_ft_in_to_m_mutant6(feet, inches):
    total_inches = feet * 10 + inches  # ❌ 10 вместо 12
    return round(total_inches * 0.0254, 2)

# Список мутантов
mutants = [
    ("Mutant 1: Wrong conversion factor (0.284)", convert_ft_in_to_m_mutant1),
    ("Mutant 2: Wrong conversion factor (0.234)", convert_ft_in_to_m_mutant2),
    ("Mutant 3: Forgot to add inches", convert_ft_in_to_m_mutant3),
    ("Mutant 4: Partial correct formula", convert_ft_in_to_m_mutant4),
    ("Mutant 5: No rounding", convert_ft_in_to_m_mutant5),
    ("Mutant 6: Wrong feet-to-inches factor", convert_ft_in_to_m_mutant6),
]

# Функция для запуска теста с подменённой функцией
def run_test_with_mutant(mutant_func):
    # Подменяем функцию в модуле
    bmi_calculator.convert_ft_in_to_m = mutant_func

    # Перезагружаем тест (чтобы использовать изменённый модуль)
    if 'test_bmi_calculator' in sys.modules:
        importlib.reload(sys.modules['test_bmi_calculator'])
    from new_test_bmi_calculator import test_convert_ft_in_to_m

    # Перехватываем вывод и возможные исключения
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    result = None
    try:
        test_convert_ft_in_to_m()
        result = True  # Тест прошёл
    except Exception as e:
        result = False  # Тест упал — мутант "убит"
    finally:
        sys.stdout = old_stdout

    return result, captured_output.getvalue()

# Основная логика мутационного тестирования
if __name__ == "__main__":
    print("🧪 Начинаем мутационное тестирование функции convert_ft_in_to_m...\n")
    killed = 0
    total = len(mutants)

    for name, mutant in mutants:
        print(f"🔁 Тестируем: {name}")
        survived = run_test_with_mutant(mutant)
        if not survived[0]:  # Тест упал → мутант убит
            print(f"❌ Мутант убит — тест обнаружил ошибку")
            killed += 1
        else:
            print(f"✅ Мутант выжил — тест НЕ обнаружил ошибку")
        print()

    # Восстанавливаем оригинальную функцию
    importlib.reload(bmi_calculator)

    # Отчёт
    print(f"📊 Результаты мутационного тестирования:")
    print(f"   Убито мутантов: {killed}/{total}")
    print(f"   Процент убитых: {killed/total*100:.1f}%")

    if killed == total:
        print("🎉 Отлично! Все мутанты убиты — тесты надёжны.")
    elif killed == 0:
        print("💀 Плохо! Ни один мутант не был обнаружен — тесты бесполезны.")
    else:
        print("⚠️  Некоторые мутанты выжили — нужно улучшить тесты.")