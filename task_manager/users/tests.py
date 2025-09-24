from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.mixins import LanguageMixin

User = get_user_model()


class UsersTest(LanguageMixin, TestCase):
    fixtures = ["users"]

    def setUp(self):
        """Настройка пользователей для тестов."""
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user3 = User.objects.get(pk=3)
        self.client.force_login(self.user1)

    # ----- 1. Тесты обновления пользователя -----
    def test_update_name_and_lastname(self):
        """Проверка успешного обновления имени и фамилии."""
        update_url = reverse("users:update", kwargs={"pk": self.user1.pk})
        response = self.client.post(
            update_url,
            data={
                "first_name": "Bob",
                "last_name": "Smith",
                "username": self.user1.username,
                "new_password": "",
                "new_password_confirm": "",
            },
            follow=True,
        )
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.first_name, "Bob")
        self.assertEqual(self.user1.last_name, "Smith")
        self.assertContains(response, "<td>Bob Smith</td>", html=True)
        self.assertNotContains(response, "<td>Oleg Dixon</td>", html=True)

    def test_update_username_unique_validation(self):
        """Нельзя установить существующее имя пользователя."""
        update_url = reverse("users:update", kwargs={"pk": self.user1.pk})
        response = self.client.post(
            update_url,
            data={
                "first_name": "Oleg",
                "last_name": "Dixon",
                "username": "Maria",
                "new_password": "",
                "new_password_confirm": "",
            },
        )
        form = response.context["form"]
        self.assertFormError(
            form, "username", "Пользователь с таким именем уже существует."
        )

    def test_update_username_empty(self):
        """Нельзя оставить пустое имя пользователя при обновлении."""
        update_url = reverse("users:update", kwargs={"pk": self.user1.pk})
        response = self.client.post(
            update_url,
            data={
                "first_name": "Oleg",
                "last_name": "Dixon",
                "username": "",
                "new_password": "",
                "new_password_confirm": "",
            },
        )
        form = response.context["form"]
        self.assertFormError(form, "username", "Обязательное поле.")

    def test_update_password_success(self):
        """Успешная смена пароля пользователя."""
        update_url = reverse("users:update", kwargs={"pk": self.user1.pk})
        self.client.post(
            update_url,
            data={
                "first_name": "Oleg",
                "last_name": "Dixon",
                "username": self.user1.username,
                "new_password": "new_pass123",
                "new_password_confirm": "new_pass123",
            },
            follow=True,
        )
        self.user1.refresh_from_db()
        self.assertTrue(self.user1.check_password("new_pass123"))

    def test_update_password_mismatch(self):
        """Ошибка при несоответствии нового пароля и подтверждения."""
        update_url = reverse("users:update", kwargs={"pk": self.user1.pk})
        response = self.client.post(
            update_url,
            data={
                "first_name": "Oleg",
                "last_name": "Dixon",
                "username": self.user1.username,
                "new_password": "new_pass123",
                "new_password_confirm": "different_pass",
            },
        )
        form = response.context["form"]
        self.assertFormError(
            form, None, "Новый пароль и подтверждение не совпадают"
        )

    # ----- 2. Тесты создания пользователя -----
    def test_create_user_success(self):
        """Создание нового пользователя через форму."""
        create_url = reverse("users:create")
        response = self.client.post(
            create_url,
            data={
                "first_name": "Alice",
                "last_name": "Brown",
                "username": "alice",
                "password": "alice123",
                "password_confirm": "alice123",
            },
            follow=True,
        )
        user = User.objects.get(username="alice")
        self.assertEqual(user.first_name, "Alice")
        self.assertEqual(user.last_name, "Brown")
        self.assertTrue(user.check_password("alice123"))
        self.assertContains(response, "Пользователь успешно зарегистрирован")

    def test_create_user_password_mismatch(self):
        """Ошибка при несовпадении пароля и подтверждения."""
        create_url = reverse("users:create")
        response = self.client.post(
            create_url,
            data={
                "first_name": 'София',
                "last_name": 'Дюкарева',
                "username": 'sofia',
                "password": "pass123",
                "password_confirm": "pass456",
            },
        )
        form = response.context["form"]
        self.assertFormError(form, None, "Пароли не совпадают")

    def test_create_user_username_empty(self):
        """Ошибка при создании пользователя с пустым username."""
        create_url = reverse("users:create")
        response = self.client.post(
            create_url,
            data={
                "first_name": "David",
                "last_name": "Lee",
                "username": "",
                "password": "pass123",
                "password_confirm": "pass123",
            },
        )
        form = response.context["form"]
        self.assertFormError(form, "username", "Обязательное поле.")

    def test_create_user_username_exists(self):
        """Ошибка при создании пользователя с существующим username."""
        create_url = reverse("users:create")
        response = self.client.post(
            create_url,
            data={
                "first_name": "Eve",
                "last_name": "Black",
                "username": self.user1.username,
                "password": "pass123",
                "password_confirm": "pass123",
            },
        )
        form = response.context["form"]
        self.assertFormError(
            form,
            "username",
            "Пользователь с таким именем уже существует."
        )

    # ----- 3. Тесты отправки пустой формы -----
    def test_user_creation_form_error(self):
        """Отправка пустой формы при создании пользователя."""
        response = self.client.post(reverse("users:create"), {}, follow=True)
        form = response.context["form"]
        self.assertFormError(form, "username", "Обязательное поле.")
        self.assertFormError(form, "password", "Обязательное поле.")

    def test_user_creation_success(self):
        """Успешное создание нового пользователя."""
        data = {
            "first_name": "Boby",
            "last_name": "Firston",
            "username": "Bob",
            "password": "password123",
            "password_confirm": "password123",
        }
        response = self.client.post(reverse("users:create"), data, follow=True)
        self.assertTrue(User.objects.filter(username="Bob").exists())
        self.assertContains(response, "Пользователь успешно зарегистрирован")

    # ----- 4. Тесты обновления и удаления новых пользователей -----
    def test_user_update(self):
        """Обновление username существующего пользователя."""
        self.client.force_login(self.user2)

        data = {
            "first_name": "Папа",
            "last_name": "Дюкарев",
            "username": "Papa_1",
            "new_password": "",
            "new_password_confirm": "",
        }

        response = self.client.post(
            reverse("users:update", args=[self.user2.id]),
            data,
            follow=True
        )

        self.user2.refresh_from_db()
        self.assertEqual(self.user2.username, "Papa_1")
        self.assertContains(response, "Пользователь успешно изменен")

    def test_user_delete(self):
        """Удаление существующего пользователя."""
        response = self.client.post(
            reverse("users:delete", args=[self.user1.id]), follow=True
        )
        self.assertContains(response, "Пользователь успешно удален")
        self.assertFalse(User.objects.filter(id=self.user1.id).exists())

    # ----- 5. Тесты выгрузки пользователей -----
    def test_load_users(self):
        """Проверка выгрузки всех пользователей из базы."""
        users_in_db = User.objects.all()
        self.assertEqual(len(users_in_db), 3)
        usernames = [user.username for user in users_in_db]
        self.assertIn("admin", usernames)
        self.assertIn("Papa", usernames)
        self.assertIn("Maria", usernames)
