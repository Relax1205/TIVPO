# tests/test_tdd_password.py
import unittest
from src.password_manager import PasswordManager

class TestPasswordManagerTDD(unittest.TestCase):
    """
    TDD-тесты для менеджера паролей.
    Покрывают операции хранения, извлечения, обновления, удаления и обработку ошибок.
    """

    def setUp(self):
        """Создаём новый менеджер перед каждым тестом."""
        self.pm = PasswordManager()

    # ============ Этап 1: Тесты для СОХРАНЕНИЯ и ИЗВЛЕЧЕНИЯ ============
    def test_save_and_retrieve_password(self):
        """TDD Шаг 1: Проверяем, что пароль можно сохранить и извлечь."""
        # Given: ничего
        # When: сохраняем пароль
        self.pm.save_password("Google", "user@gmail.com", "secret123")

        # Then: извлекаем и проверяем данные
        retrieved = self.pm.get_password("Google")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["login"], "user@gmail.com")
        self.assertEqual(retrieved["password"], "secret123")

    def test_retrieve_nonexistent_service_returns_none(self):
        """TDD Шаг 2: Попытка извлечь пароль для несуществующего сервиса возвращает None."""
        # Given: сервис не существует
        # When: запрашиваем пароль
        result = self.pm.get_password("NonExistentService")

        # Then: возвращается None
        self.assertIsNone(result)

    # ============ Этап 2: Тесты для ОБНОВЛЕНИЯ ============
    def test_update_password_successfully(self):
        """TDD Шаг 3: Пароль можно успешно обновить для существующего сервиса."""
        # Given: сохранённый пароль
        self.pm.save_password("VK", "mylogin", "old_password")

        # When: обновляем пароль
        success = self.pm.update_password("VK", "new_secure_password")

        # Then: обновление успешно
        self.assertTrue(success)

        # Then: извлекаем и проверяем новый пароль
        updated = self.pm.get_password("VK")
        self.assertEqual(updated["password"], "new_secure_password")

    def test_update_nonexistent_service_returns_false(self):
        """TDD Шаг 4: Попытка обновить пароль для несуществующего сервиса возвращает False."""
        # Given: сервис не существует
        # When: пытаемся обновить пароль
        success = self.pm.update_password("Twitter", "new_pass")

        # Then: возвращается False
        self.assertFalse(success)

    def test_update_password_with_empty_string_raises_error(self):
        """TDD Шаг 5: Обновление пароля пустой строкой вызывает ValueError."""
        # Given: сохранённый сервис
        self.pm.save_password("Facebook", "fbuser", "old_pass")

        # When/Then: ожидаем исключение
        with self.assertRaises(ValueError) as context:
            self.pm.update_password("Facebook", "")

        self.assertIn("не может быть пустым", str(context.exception))

    # ============ Этап 3: Тесты для УДАЛЕНИЯ ============
    def test_delete_password_successfully(self):
        """TDD Шаг 6: Пароль можно успешно удалить."""
        # Given: сохранённый пароль
        self.pm.save_password("GitHub", "mygithub", "gh_token")

        # When: удаляем пароль
        success = self.pm.delete_password("GitHub")

        # Then: удаление успешно
        self.assertTrue(success)

        # Then: сервис больше не существует
        self.assertIsNone(self.pm.get_password("GitHub"))

    def test_delete_nonexistent_service_returns_false(self):
        """TDD Шаг 7: Попытка удалить несуществующий сервис возвращает False."""
        # Given: сервис не существует
        # When: пытаемся удалить
        success = self.pm.delete_password("LinkedIn")

        # Then: возвращается False
        self.assertFalse(success)

    # ============ Этап 4: Тесты для ОБРАБОТКИ ОШИБОК ============
    def test_save_password_with_empty_service_name_raises_error(self):
        """TDD Шаг 8: Попытка сохранить пароль с пустым именем сервиса вызывает ValueError."""
        with self.assertRaises(ValueError) as context:
            self.pm.save_password("", "user", "pass")
        self.assertIn("не могут быть пустыми", str(context.exception))

    def test_save_password_with_empty_login_raises_error(self):
        """TDD Шаг 9: Попытка сохранить пароль с пустым логином вызывает ValueError."""
        with self.assertRaises(ValueError) as context:
            self.pm.save_password("Service", "", "pass")
        self.assertIn("не могут быть пустыми", str(context.exception))

    def test_save_password_with_empty_password_raises_error(self):
        """TDD Шаг 10: Попытка сохранить пароль с пустым паролем вызывает ValueError."""
        with self.assertRaises(ValueError) as context:
            self.pm.save_password("Service", "login", "")
        self.assertIn("не могут быть пустыми", str(context.exception))

    # ============ Дополнительный тест: Проверка list_services ============
    def test_list_services_returns_correct_service_names(self):
        """TDD Шаг 11: list_services возвращает правильный список имён сервисов."""
        # Given: несколько сервисов
        self.pm.save_password("Google", "user1", "pass1")
        self.pm.save_password("VK", "user2", "pass2")
        self.pm.save_password("GitHub", "user3", "pass3")

        # When: запрашиваем список
        services = self.pm.list_services()

        # Then: возвращается список из 3 элементов
        self.assertEqual(len(services), 3)
        self.assertIn("Google", services)
        self.assertIn("VK", services)
        self.assertIn("GitHub", services)


if __name__ == "__main__":
    unittest.main(verbosity=2)