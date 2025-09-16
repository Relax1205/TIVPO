# demo_password.py
from src.password_manager import PasswordManager

def main():
    # Создаём менеджер паролей
    pm = PasswordManager()

    # Сохраняем пароли
    pm.save_password("Google", "user@gmail.com", "secret123")
    pm.save_password("VK", "mylogin", "vkpass456")
    pm.save_password("GitHub", "mygithub", "gh_token789")

    # Извлекаем пароль
    google_data = pm.get_password("Google")
    print("🔐 Данные для Google:")
    print(f"   Логин: {google_data['login']}")
    print(f"   Пароль: {google_data['password']}")

    # Обновляем пароль
    pm.update_password("VK", "new_vk_password")
    vk_data = pm.get_password("VK")
    print("\n🔐 Обновлённые данные для VK:")
    print(f"   Пароль: {vk_data['password']}")

    # Удаляем пароль
    pm.delete_password("GitHub")
    print(f"\n🗑️  GitHub удалён. Оставшиеся сервисы: {pm.list_services()}")

    # Попытка получить несуществующий сервис
    netflix = pm.get_password("Netflix")
    print(f"\n❓ Netflix: {'Не найден' if netflix is None else netflix}")


if __name__ == "__main__":
    main()