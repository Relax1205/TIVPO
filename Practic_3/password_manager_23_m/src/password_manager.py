# src/password_manager.py
from typing import Dict, Optional, List

class PasswordManager:
    """
    Менеджер паролей.
    Позволяет сохранять, извлекать, обновлять и удалять пароли для различных сервисов.
    """

    def __init__(self):
        self.passwords: Dict[str, Dict[str, str]] = {}  # {service_name: {"login": "...", "password": "..."}}

    def save_password(self, service_name: str, login: str, password: str) -> bool:
        """
        Сохраняет или обновляет пароль для указанного сервиса.
        
        :param service_name: Название сервиса (например, "Google", "VK")
        :param login: Логин пользователя
        :param password: Пароль
        :return: True, если успешно сохранено/обновлено
        """
        if not service_name or not login or not password:
            raise ValueError("Название сервиса, логин и пароль не могут быть пустыми")

        self.passwords[service_name] = {
            "login": login,
            "password": password
        }
        return True

    def get_password(self, service_name: str) -> Optional[Dict[str, str]]:
        """
        Извлекает пароль для указанного сервиса.
        
        :param service_name: Название сервиса
        :return: Словарь с логином и паролем, или None, если сервис не найден
        """
        return self.passwords.get(service_name)

    def update_password(self, service_name: str, new_password: str) -> bool:
        """
        Обновляет пароль для существующего сервиса.
        
        :param service_name: Название сервиса
        :param new_password: Новый пароль
        :return: True, если успешно обновлено; False, если сервис не найден
        :raises ValueError: если пароль пустой
        """
        if not new_password:
            raise ValueError("Новый пароль не может быть пустым")

        if service_name not in self.passwords:
            return False

        self.passwords[service_name]["password"] = new_password
        return True

    def delete_password(self, service_name: str) -> bool:
        """
        Удаляет пароль для указанного сервиса.
        
        :param service_name: Название сервиса
        :return: True, если успешно удалено; False, если сервис не найден
        """
        if service_name in self.passwords:
            del self.passwords[service_name]
            return True
        return False

    def list_services(self) -> List[str]:
        """
        Возвращает список всех сохранённых сервисов.
        
        :return: Список названий сервисов
        """
        return list(self.passwords.keys())