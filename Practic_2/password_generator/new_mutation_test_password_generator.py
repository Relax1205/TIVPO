# new_mutation_test_password_generator.py

import importlib
import sys
import unittest
from io import StringIO

# Импортируем основной модуль
import password_generator


# --- 🔥 Мутанты: check_password_strength ---


def check_password_strength_mutant1(password):
    """Не проверяет символы"""
    if (password_generator.has_uppercase(password) and
        password_generator.has_lowercase(password) and
        password_generator.has_digits(password)):
        return "strong"
    return "weak"

def check_password_strength_mutant2(password):
    """Не проверяет строчные буквы"""
    if (password_generator.has_uppercase(password) and
        password_generator.has_digits(password) and
        any(c in "!@#$%&*" for c in password)):
        return "strong"
    return "weak"

def check_password_strength_mutant3(password):
    """Всегда возвращает 'strong'"""
    return "strong"

def check_password_strength_mutant4(password):
    """Всегда возвращает 'weak'"""
    return "weak"


# --- 🔧 Мутанты: generate_password ---

def generate_password_mutant1(length, use_upper=True, use_lower=True, use_digits=True, use_symbols=True):
    """Не гарантирует хотя бы по одному символу каждого типа"""
    if length < 4:
        raise ValueError("Длина пароля должна быть не менее 4 символов.")
    characters = ""
    if use_lower:
        characters += "abcdefghijklmnopqrstuvwxyz"
    if use_upper:
        characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if use_digits:
        characters += "0123456789"
    if use_symbols:
        characters += "!@#$%&*"
    if not characters:
        raise ValueError("Не выбрано ни одного типа символов.")
    # ❌ Нет гарантии включения всех типов
    return ''.join(random.choice(characters) for _ in range(length))


def generate_password_mutant2(length, use_upper=True, use_lower=True, use_digits=True, use_symbols=True):
    """Не перемешивает пароль (сначала фиксированные символы)"""
    if length < 4:
        raise ValueError("Длина пароля должна быть не менее 4 символов.")
    password = []
    if use_lower:
        password.append(random.choice("abcdefghijklmnopqrstuvwxyz"))
    if use_upper:
        password.append(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    if use_digits:
        password.append(random.choice("0123456789"))
    if use_symbols:
        password.append(random.choice("!@#$%&*"))
    characters = "".join(filter(None, [
        "abcdefghijklmnopqrstuvwxyz" if use_lower else "",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if use_upper else "",
        "0123456789" if use_digits else "",
        "!@#$%&*" if use_symbols else ""
    ]))
    for _ in range(length - len(password)):
        password.append(random.choice(characters))
    # ❌ Нет random.shuffle(password)
    return ''.join(password)


# --- 🔤 Мутанты: вспомогательные функции ---

def has_uppercase_mutant(password):
    """Ошибочно считает, что 'I' — не заглавная"""
    return any(c.isupper() for c in password if c != 'I')

def has_lowercase_mutant(password):
    """Считает только первые 3 символа"""
    return any(c.islower() for c in password[:3])

def has_digits_mutant(password):
    """Считает только '1', '3', '5', '7', '9' (чётные пропущены)"""
    return any(c in "13579" for c in password)


# --- 🧬 Полный список мутантов ---
mutants = [
    # Проверка сложности
    ("Mutant 1: No symbol check", check_password_strength_mutant1, "check_password_strength"),
    ("Mutant 2: No lowercase check", check_password_strength_mutant2, "check_password_strength"),
    ("Mutant 3: Always strong", check_password_strength_mutant3, "check_password_strength"),
    ("Mutant 4: Always weak", check_password_strength_mutant4, "check_password_strength"),

    # Генерация пароля
    ("Mutant 5: No guaranteed chars", generate_password_mutant1, "generate_password"),
    ("Mutant 6: No shuffle", generate_password_mutant2, "generate_password"),

    ("Mutant 7: has_digits misses even digits", has_digits_mutant, "has_digits"),
]


# --- 🧪 Запуск всех тестов ---
def run_all_tests(test_module_name):
    """Запускает все тесты и возвращает True, если все прошли"""
    if test_module_name in sys.modules:
        importlib.reload(sys.modules[test_module_name])
    else:
        try:
            importlib.import_module(test_module_name)
        except ModuleNotFoundError:
            print(f"❌ Не найден модуль: {test_module_name}")
            return False

    test_stream = StringIO()
    runner = unittest.TextTestRunner(stream=test_stream, verbosity=0)
    suite = unittest.TestLoader().loadTestsFromName(test_module_name)
    result = runner.run(suite)

    # Возвращаем True, если нет ошибок и падений
    return len(result.failures) == 0 and len(result.errors) == 0


# --- 🧫 Основной цикл мутационного тестирования ---
if __name__ == "__main__":
    print("🧪 Начинаем мутационное тестирование: password_generator\n")
    killed = 0
    total = len(mutants)

    for name, mutant_func, func_name in mutants:
        print(f"🔁 Тестируем: {name}")

        # Сохраняем оригинальную функцию
        if not hasattr(password_generator, func_name):
            print(f"❌ Функция {func_name} не найдена в модуле")
            continue

        original_func = getattr(password_generator, func_name)
        setattr(password_generator, func_name, mutant_func)

        # Запускаем тесты
        all_tests_passed = run_all_tests('new_test_password_generator')

        # Восстанавливаем
        setattr(password_generator, func_name, original_func)

        if all_tests_passed:
            print(f"✅ Мутант выжил — все тесты прошли")
        else:
            print(f"❌ Мутант убит — хотя бы один тест упал")
            killed += 1
        print()

    # 📊 Отчёт
    print(f"📊 Результаты мутационного тестирования:")
    print(f"   Убито мутантов: {killed}/{total}")
    print(f"   Процент убитых: {killed / total * 100:.1f}%")

    if killed == total:
        print("🎉 Отлично! Все мутанты убиты — тесты надёжны.")
    elif killed == 0:
        print("💀 Плохо! Ни один мутант не был обнаружен — тесты бесполезны.")
    else:
        surviving = total - killed
        print(f"⚠️  {surviving} мутантов выжили — нужно улучшить тесты.")