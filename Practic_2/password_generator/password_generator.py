import random
import string


def generate_password(length, use_upper=True, use_lower=True, use_digits=True, use_symbols=True):
    """
    Генерирует случайный пароль заданной длины с опциональными символами.
    :param length: длина пароля (целое число, >= 4)
    :param use_upper: использовать ли заглавные буквы
    :param use_lower: использовать ли строчные буквы
    :param use_digits: использовать ли цифры
    :param use_symbols: использовать ли символы (!@#$%...)
    :return: сгенерированный пароль (строка)
    """
    if length < 4:
        raise ValueError("Длина пароля должна быть не менее 4 символов.")
    
    characters = ""
    if use_lower:
        characters += string.ascii_lowercase
    if use_upper:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += "!@#$%&*"

    if not characters:
        raise ValueError("Не выбрано ни одного типа символов.")

    password = []
    # Гарантируем хотя бы по одному символу каждого выбранного типа
    if use_lower:
        password.append(random.choice(string.ascii_lowercase))
    if use_upper:
        password.append(random.choice(string.ascii_uppercase))
    if use_digits:
        password.append(random.choice(string.digits))
    if use_symbols:
        password.append(random.choice("!@#$%&*"))

    # Заполняем оставшееся случайными символами
    for _ in range(length - len(password)):
        password.append(random.choice(characters))

    random.shuffle(password)
    return ''.join(password)


def has_uppercase(password):
    """
    Проверяет, содержит ли пароль хотя бы одну заглавную букву.
    :param password: строка пароля
    :return: True, если есть заглавная буква
    """
    return any(c.isupper() for c in password)


def has_lowercase(password):
    """
    Проверяет, содержит ли пароль хотя бы одну строчную букву.
    :param password: строка пароля
    :return: True, если есть строчная буква
    """
    return any(c.islower() for c in password)


def has_digits(password):
    """
    Проверяет, содержит ли пароль хотя бы одну цифру.
    :param password: строка пароля
    :return: True, если есть цифра
    """
    return any(c.isdigit() for c in password)



# Намеренная ошибка 

# def check_password_strength(password):
#     """
#     Оценивает сложность пароля.
#     Преднамеренная ошибка: не проверяются цифры (пропущено условие has_digits).
#     :param password: пароль
#     :return: 'strong', если пароль содержит верхний, нижний регистр и символы;
#              иначе 'weak'
#     """
#     if (has_uppercase(password) and 
#         has_lowercase(password) and 
#         any(c in "!@#$%&*" for c in password)):  # ОШИБКА: нет проверки на цифры!
#         return "strongest"
#     return "weak"



# #  Исправленная версия

def check_password_strength(password):
    if (has_uppercase(password) and 
        has_lowercase(password) and 
        any(c in "!@#$%&*" for c in password)):
        return "strong"
    return "weak"
