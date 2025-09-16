# tests/test_atdd_password.py
import unittest
from src.password_manager import PasswordManager

class TestPasswordManagerATDD(unittest.TestCase):
    """
    ATDD-тесты для менеджера паролей.
    Моделируют сценарии защиты данных с точки зрения пользователя.
    Согласованы с "заказчиком" как приёмочные критерии безопасности.
    """

    def setUp(self):
        """Создаём новый менеджер перед каждым тестом."""
        self.pm = PasswordManager()

    # ============ Сценарий 1: Защита от сохранения пустых данных ============
    def test_user_cannot_save_password_with_empty_fields(self):
        """
        ATDD Сценарий 1 (Защита данных):
        Given: Пользователь пытается сохранить пароль с пустым названием сервиса
        When: Вызывает save_password("", "login", "password")
        Then: Система выбрасывает ValueError с сообщением об ошибке
        And: Пароль не сохраняется в системе
        """
        # When/Then: ожидаем исключение
        with self.assertRaises(ValueError) as context:
            self.pm.save_password("", "user", "pass123")

        # Then: проверяем сообщение об ошибке
        self.assertIn("не могут быть пустыми", str(context.exception))

        # And: проверяем, что ничего не сохранилось
        self.assertEqual(len(self.pm.list_services()), 0)

    # ============ Сценарий 2: Защита от доступа к несуществующему сервису ============
    def test_user_sees_error_when_requesting_nonexistent_service(self):
        """
        ATDD Сценарий 2 (Защита данных):
        Given: Сервис "Netflix" не существует в системе
        When: Пользователь запрашивает пароль для "Netflix"
        Then: Система возвращает None
        And: Пользователь видит сообщение "Сервис не найден."
        """
        # When
        result = self.pm.get_password("Netflix")

        # Then
        self.assertIsNone(result)

        # And: эмулируем отображение сообщения в UI
        display_message = "Сервис не найден." if result is None else ""
        self.assertEqual(display_message, "Сервис не найден.")

    # ============ Сценарий 3: Защита при обновлении несуществующего сервиса ============
    def test_user_cannot_update_password_for_nonexistent_service(self):
        """
        ATDD Сценарий 3 (Защита данных):
        Given: Сервис "Twitter" не существует в системе
        When: Пользователь пытается обновить пароль для "Twitter"
        Then: Система возвращает False
        And: Никакие данные не изменяются
        """
        # When
        success = self.pm.update_password("Twitter", "new_password")

        # Then
        self.assertFalse(success)

        # And: проверяем, что список сервисов пуст
        self.assertEqual(len(self.pm.list_services()), 0)

    # ============ Сценарий 4: Защита целостности данных при удалении ============
    def test_deleted_password_is_inaccessible_and_not_listed(self):
        """
        ATDD Сценарий 4 (Защита данных):
        Given: Пароль для "Google" сохранён в системе
        When: Пользователь удаляет пароль для "Google"
        Then: Попытка получить пароль для "Google" возвращает None
        And: "Google" не отображается в списке сервисов
        """
        # Given
        self.pm.save_password("Google", "user@gmail.com", "secret123")

        # When
        self.pm.delete_password("Google")

        # Then
        retrieved = self.pm.get_password("Google")
        self.assertIsNone(retrieved)

        # And
        services = self.pm.list_services()
        self.assertNotIn("Google", services)
        self.assertEqual(len(services), 0)

    # ============ Сценарий 5: Визуализация безопасности — список сервисов без паролей ============
    def test_user_can_see_only_service_names_without_passwords(self):
        """
        ATDD Сценарий 5 (Защита данных):
        Given: В системе сохранены пароли для "VK" и "GitHub"
        When: Пользователь запрашивает список сервисов
        Then: Возвращается список ["VK", "GitHub"]
        And: Ни в одном элементе списка не содержится пароль (только названия)
        """
        # Given
        self.pm.save_password("VK", "mylogin", "vkpass")
        self.pm.save_password("GitHub", "mygithub", "ghtoken")

        # When
        services = self.pm.list_services()

        # Then
        self.assertEqual(len(services), 2)
        self.assertIn("VK", services)
        self.assertIn("GitHub", services)

        # And: убеждаемся, что это только строки — названия, без паролей
        for service_name in services:
            self.assertIsInstance(service_name, str)
            # Дополнительно: убедимся, что пароли не "утекают" в список
            # (в нашей реализации list_services возвращает только ключи — это безопасно)
            self.assertNotIn("pass", service_name.lower())
            self.assertNotIn("token", service_name.lower())
            self.assertNotIn("secret", service_name.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)