from .models import Status
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class AuthTestCase(TestCase):
    """Базовый класс для тестов с авторизованным пользователем"""
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.login(username="testuser", password="password123")


class StatusesTest(AuthTestCase):
    fixtures = ["statuses.json"]

    # ----- 1. Тесты обновления статуса -----
    def test_update_status(self):
        """Проверка успешного обновления статуса"""
        update_url = reverse('statuses:update', kwargs={'pk': 1})
        response = self.client.post(
            update_url,
            data={
                "name": "В работе",
            },
            follow=True
        )
        status = Status.objects.get(pk=1)
        self.assertEqual(status.name, "В работе")

        self.assertContains(response, "<td>В работе</td>", html=True)
        self.assertNotContains(response, "<td>Уже в работе</td>", html=True)

    
    # def test_update_username_unique_validation(self):
    #     """Нельзя установить существующее имя пользователя"""
    #     update_url = reverse('users:update', kwargs={'pk': 1})
    #     response = self.client.post(
    #         update_url,
    #         data={
    #             "first_name": "Oleg",
    #             "last_name": "Dixon",
    #             "username": "Maria",
    #             "new_password": "",
    #             "new_password_confirm": ""
    #         }
    #     )
    #     form = response.context['form']
    #     self.assertFormError(
    #         form, 
    #         'username',
    #         'Пользователь с таким именем уже существует.'
    #     )

    # def test_update_username_empty(self):
    #     """Нельзя оставить пустое имя пользователя при обновлении"""
    #     update_url = reverse('users:update', kwargs={'pk': 1})
    #     response = self.client.post(
    #         update_url,
    #         data={
    #             "first_name": "Oleg",
    #             "last_name": "Dixon",
    #             "username": "",
    #             "new_password": "",
    #             "new_password_confirm": ""
    #         }
    #     )
    #     form = response.context['form']
    #     self.assertFormError(
    #         form,
    #         'username',
    #         'This field is required.'
    #     )

    # def test_update_password_success(self):
    #     """Проверка успешного изменения пароля"""
    #     update_url = reverse('users:update', kwargs={'pk': 1})
    #     response = self.client.post(
    #         update_url,
    #         data={
    #             "first_name": "Oleg",
    #             "last_name": "Dixon",
    #             "username": "admin",
    #             "new_password": "new_pass123",
    #             "new_password_confirm": "new_pass123"
    #         },
    #         follow=True
    #     )
    #     user = User.objects.get(pk=1)
    #     self.assertTrue(user.check_password("new_pass123"))

    # def test_update_password_mismatch(self):
    #     """Ошибка при несоответствии нового пароля и подтверждения"""
    #     update_url = reverse('users:update', kwargs={'pk': 1})
    #     response = self.client.post(
    #         update_url,
    #         data={
    #             "first_name": "Oleg",
    #             "last_name": "Dixon",
    #             "username": "admin",
    #             "new_password": "new_pass123",
    #             "new_password_confirm": "different_pass"
    #         }
    #     )
    #     form = response.context['form']
    #     self.assertFormError(
    #         form, 
    #         None,
    #         "Новый пароль и подтверждение не совпадают"
    #     )

    # # # ----- 2. Тесты создания пользователя -----
    # def test_create_user_success(self):
    #     """Создание нового пользователя через форму"""
    #     create_url = reverse('users:create')
    #     response = self.client.post(
    #         create_url,
    #         data={
    #             "first_name": "Alice",
    #             "last_name": "Brown",
    #             "username": "alice",
    #             "password": "alice123",
    #             "password_confirm": "alice123"
    #         },
    #         follow=True
    #     )
    #     user = User.objects.get(username="alice")
    #     self.assertEqual(user.first_name, "Alice")
    #     self.assertEqual(user.last_name, "Brown")
    #     self.assertTrue(user.check_password("alice123"))
    #     response = self.client.get(reverse('users:index'))
    #     self.assertContains(response, "Alice Brown")

    # def test_create_user_password_mismatch(self):
    #     """Ошибка при несовпадении пароля и подтверждения"""
    #     create_url = reverse('users:create')
    #     response = self.client.post(
    #         create_url,
    #         data={
    #             "first_name": "Charlie",
    #             "last_name": "Green",
    #             "username": "charlie",
    #             "password": "pass123",
    #             "password_confirm": "pass456"
    #         }
    #     )
    #     form = response.context['form']
    #     self.assertFormError(
    #         form,
    #         None,
    #         "Пароли не совпадают"
    #     )

    # def test_create_user_username_empty(self):
    #     """Ошибка при создании пользователя с пустым username"""
    #     create_url = reverse('users:create')
    #     response = self.client.post(
    #         create_url,
    #         data={
    #             "first_name": "David",
    #             "last_name": "Lee",
    #             "username": "",
    #             "password": "pass123",
    #             "password_confirm": "pass123"
    #         }
    #     )
    #     form = response.context['form']
    #     self.assertFormError(
    #         form,
    #         'username',
    #         'This field is required.'
    #     )

    # def test_create_user_username_exists(self):
    #     """Ошибка при создании пользователя с существующим username"""
    #     create_url = reverse('users:create')
    #     response = self.client.post(
    #         create_url,
    #         data={
    #             "first_name": "Eve",
    #             "last_name": "Black",
    #             "username": "admin",
    #             "password": "pass123",
    #             "password_confirm": "pass123"
    #         }
    #     )
    #     form = response.context['form']
    #     self.assertFormError(
    #         form,
    #         'username',
    #         'Пользователь с таким именем уже существует.'
    #     )

    # # # ----- 3. Тесты новых пользователей -----
    # def test_user_creation_form_error(self):
    #     """Отправка пустой формы при создании пользователя"""
    #     response = self.client.post(reverse('users:create'), {}, follow=True)
    #     form = response.context['form']
    #     self.assertFormError(
    #         form,
    #         'username',
    #         'This field is required.'
    #     )
    #     self.assertFormError(
    #         form,
    #         'password',
    #         'This field is required.'
    #     )

    # def test_user_creation_success(self):
    #     """Успешное создание нового пользователя"""
    #     data = {
    #         "first_name": "Boby",
    #         "last_name": "Firston",
    #         'username': 'Bob',
    #         'password': 'password123',
    #         'password_confirm': 'password123',
    #     }
    #     response = self.client.post(reverse('users:create'), data, follow=True)

    
    #     self.assertTrue(User.objects.filter(username="Bob").exists())
    #     self.assertContains(response, "Пользователь успешно зарегистрирован")

    # # # ----- 4. Тесты обновления и удаления нового пользователя -----
    # def test_user_update(self):
    #     """Обновление username существующего пользователя"""
    #     data = {
    #         "first_name": "Alisha",
    #         "last_name": "Perkinton",
    #         'username': 'AliceUpdated',
    #         'password': 'pswd555',
    #         'password_confirm': 'pswd555',
    #     }
    #     response = self.client.post(
    #         reverse('users:update', args=[self.user1.id]),
    #         data,
    #         follow=True
    #     )
    #     self.user1.refresh_from_db()
    #     self.assertEqual(self.user1.username, 'AliceUpdated')
    #     self.assertContains(response, 'Пользователь успешно изменен')

    # def test_user_delete(self):
    #     """Удаление существующего пользователя"""
    #     response = self.client.post(
    #         reverse('users:delete', args=[self.user2.id]),
    #         follow=True
    #     )
    #     self.assertContains(response, 'Пользователь успешно удален')
    #     self.assertFalse(User.objects.filter(id=self.user2.id).exists())
