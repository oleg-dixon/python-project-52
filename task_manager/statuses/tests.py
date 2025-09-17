from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Status
from task_manager.mixins import LanguageMixin


class AuthTestCase(TestCase):
    """Базовый класс для тестов с авторизованным пользователем"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.login(username="testuser", password="password123")
        

class StatusesTest(LanguageMixin, AuthTestCase):
    fixtures = ["statuses.json"]

    # ----- 1. Тесты обновления статуса -----
    def test_update_status(self):
        """Проверка успешного обновления статуса"""
        update_url = reverse('statuses:update', kwargs={'pk': 1})
        response = self.client.post(
            update_url,
            data={"name": "В работе"},
            follow=True
        )
        status = Status.objects.get(pk=1)
        self.assertEqual(status.name, "В работе")
        self.assertContains(response, "<td>В работе</td>", html=True)
        self.assertNotContains(response, "<td>Уже в работе</td>", html=True)

    def test_update_status_unique_validation(self):
        """Нельзя установить существующее название статуса"""
        update_url = reverse('statuses:update', kwargs={'pk': 1})
        response = self.client.post(
            update_url,
            data={"name": "На рассмотрении"}
        )
        form = response.context['form']
        self.assertFormError(
            form,
            'name',
            'Статус с таким названием уже существует.'
        )

    def test_update_status_empty(self):
        """Нельзя оставить пустое название статуса"""
        update_url = reverse('statuses:update', kwargs={'pk': 1})
        response = self.client.post(update_url, data={"name": ""})
        form = response.context['form']
        self.assertFormError(form, 'name', 'Обязательное поле.')

    # ----- 2. Тесты создания статуса -----
    def test_create_status_success(self):
        """Создание нового статуса через форму"""
        create_url = reverse('statuses:create')
        response = self.client.post(
            create_url,
            data={"name": "В продакшен"},
            follow=True
        )
        status = Status.objects.get(name="В продакшен")
        self.assertEqual(status.name, "В продакшен")
        self.assertContains(response, "Статус успешно создан")

    def test_create_status_unique_validation(self):
        """Нельзя создать статус с уже существующим названием"""
        create_url = reverse('statuses:create')
        response = self.client.post(
            create_url,
            data={"name": "На рассмотрении"}
        )
        form = response.context['form']
        self.assertFormError(
            form,
            'name',
            'Статус с таким названием уже существует.'
        )

    def test_status_creation_form_error(self):
        """Отправка пустой формы при создании статуса"""
        response = self.client.post(reverse('statuses:create'), {}, follow=True)
        form = response.context['form']
        self.assertFormError(form, 'name', 'Обязательное поле.')

    # ----- 3. Тесты удаления статуса -----
    def test_status_delete(self):
        """Удаление существующего статуса"""
        status_to_delete = Status.objects.create(name="Удаляемый статус")
        response = self.client.post(
            reverse('statuses:delete', kwargs={'pk': status_to_delete.pk}),
            follow=True
        )
        self.assertContains(response, 'Статус успешно удален')
        self.assertFalse(Status.objects.filter(pk=status_to_delete.pk).exists())
