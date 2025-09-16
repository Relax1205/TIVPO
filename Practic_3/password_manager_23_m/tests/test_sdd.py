# tests/test_sdd_password.py
import unittest
from src.password_manager import PasswordManager

class TestPasswordManagerSDD(unittest.TestCase):
    """
    SDD-тесты для менеджера паролей.
    На основе спецификации с примерами данных паролей и условий доступа.
    Спецификация находится в specs/password_specifications.md
    """

    def setUp(self):
        """Создаём новый менеджер перед каждым тестом."""
        self.pm = PasswordManager()

    # ============ Тест 1: Проверка примеров из Таблицы 1 (Сохранение и извлечение) ============
    def test_sdd_specification_table1_save_and_retrieve(self):
        """
        SDD Тест 1: Проверка сохранения и извлечения по Таблице 1 спецификации.
        """
        test_cases = [
            ("Google", "user@gmail.com", "secret123"),
            ("VK", "my_vk_login", "vk_pass!@#"),
            ("GitHub", "dev_user", "ghp_tokenXYZ")
        ]

        for service, login, password in test_cases:
            # When: сохраняем пароль
            success = self.pm.save_password(service, login, password)
            self.assertTrue(success, f"Сохранение для {service} должно быть успешным")

            # When: извлекаем пароль
            retrieved = self.pm.get_password(service)

            # Then: проверяем данные
            self.assertIsNotNone(retrieved, f"Данные для {service} не должны быть None")
            self.assertEqual(retrieved["login"], login, f"Логин для {service} не совпадает")
            self.assertEqual(retrieved["password"], password, f"Пароль для {service} не совпадает")

    # ============ Тест 2: Проверка примеров из Таблицы 2 (Обработка ошибок) ============
    def test_sdd_specification_table2_error_handling(self):
        """
        SDD Тест 2: Проверка обработки ошибок при сохранении (Таблица 2).
        """
        error_cases = [
            ("", "user@gmail.com", "secret123"),
            ("Google", "", "secret123"),
            ("Google", "user@gmail.com", "")
        ]

        for service, login, password in error_cases:
            with self.assertRaises(ValueError) as context:
                self.pm.save_password(service, login, password)
            self.assertIn("не могут быть пустыми", str(context.exception))

    # ============ Тест 3: Проверка примеров из Таблицы 3 (Обновление паролей) ============
    def test_sdd_specification_table3_update_password(self):
        """
        SDD Тест 3: Проверка обновления паролей (Таблица 3).
        """
        # Given: сохраняем исходный пароль
        self.pm.save_password("Google", "user@gmail.com", "secret123")

        # When: обновляем пароль
        success = self.pm.update_password("Google", "new_google_pwd")

        # Then: обновление успешно
        self.assertTrue(success)

        # Then: извлекаем и проверяем новый пароль
        updated = self.pm.get_password("Google")
        self.assertEqual(updated["password"], "new_google_pwd")

        # When: пытаемся обновить несуществующий сервис
        success_twitter = self.pm.update_password("Twitter", "new_twitter_pwd")

        # Then: возвращается False
        self.assertFalse(success_twitter)

    # ============ Тест 4: Проверка примеров из Таблицы 4 (Удаление паролей) ============
    def test_sdd_specification_table4_delete_password(self):
        """
        SDD Тест 4: Проверка удаления паролей (Таблица 4).
        """
        # Given: сохраняем пароль
        self.pm.save_password("GitHub", "dev_user", "ghp_tokenXYZ")

        # When: удаляем пароль
        success = self.pm.delete_password("GitHub")

        # Then: удаление успешно
        self.assertTrue(success)

        # Then: сервис больше не существует
        self.assertIsNone(self.pm.get_password("GitHub"))

        # When: пытаемся удалить несуществующий сервис
        success_linkedin = self.pm.delete_password("LinkedIn")

        # Then: возвращается False
        self.assertFalse(success_linkedin)

    # ============ Тест 5: Проверка граничных случаев из Таблицы 5 ============
    def test_sdd_specification_table5_edge_cases(self):
        """
        SDD Тест 5: Проверка граничных случаев и условий доступа (Таблица 5).
        """
        # Сценарий 1: Получение несуществующего сервиса
        result = self.pm.get_password("NonExistentService")
        self.assertIsNone(result)

        # Сценарий 2: Обновление пароля на пустую строку
        self.pm.save_password("Google", "user", "old_pass")
        with self.assertRaises(ValueError) as context:
            self.pm.update_password("Google", "")
        self.assertIn("не может быть пустым", str(context.exception))

        # Сценарий 3: Сохранение дубликата сервиса (должно перезаписывать)
        self.pm.save_password("Google", "user1", "pass1")
        self.pm.save_password("Google", "user2", "pass2")  # перезапись

        retrieved = self.pm.get_password("Google")
        self.assertEqual(retrieved["login"], "user2")
        self.assertEqual(retrieved["password"], "pass2")


if __name__ == "__main__":
    unittest.main(verbosity=2)