from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.mixins import LanguageMixin

from .models import Label


class AuthTestCase(TestCase):
    """Базовый класс для тестов с авторизованным пользователем"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.login(username="testuser", password="password123")
        

class LabelsTest(LanguageMixin, AuthTestCase):
    fixtures = ["labels.json"]

    # ----- 1. Тесты обновления метки -----
    def test_update_label(self):
        """Проверка успешного обновления метки"""
        update_url = reverse('labels:update', kwargs={'pk': 1})
        response = self.client.post(
            update_url,
            data={"name": "Дела"},
            follow=True
        )
        label = Label.objects.get(pk=1)
        self.assertEqual(label.name, "Дела")
        self.assertContains(response, "<td>Дела</td>", html=True)
        self.assertNotContains(response, "<td>Дом</td>", html=True)

    def test_update_label_unique_validation(self):
        """Нельзя установить существующее название метки"""
        update_url = reverse('labels:update', kwargs={'pk': 1})
        response = self.client.post(
            update_url,
            data={"name": "Работа"}
        )

        form = response.context['form']
        self.assertFormError(
            form,
            'name',
            'Метка с таким названием уже существует.'
        )

    def test_update_label_empty(self):
        """Нельзя оставить пустое название метки"""
        update_url = reverse('labels:update', kwargs={'pk': 1})
        response = self.client.post(update_url, data={"name": ""})
        form = response.context['form']
        self.assertFormError(form, 'name', 'Обязательное поле.')

    # ----- 2. Тесты создания метки -----
    def test_create_label_success(self):
        """Создание новой метки через форму"""
        create_url = reverse('labels:create')
        response = self.client.post(
            create_url,
            data={"name": "Продакшен"},
            follow=True
        )
        label = Label.objects.get(name="Продакшен")
        self.assertEqual(label.name, "Продакшен")
        self.assertContains(response, "Метка успешно создана")

    def test_create_label_unique_validation(self):
        """Нельзя создать метку с уже существующим названием"""
        create_url = reverse('labels:create')
        response = self.client.post(
            create_url,
            data={"name": "Работа"}
        )
        form = response.context['form']
        self.assertFormError(
            form,
            'name',
            'Метка с таким названием уже существует.'
        )

    def test_label_creation_form_error(self):
        """Отправка пустой формы при создании метки"""
        response = self.client.post(reverse('labels:create'), {}, follow=True)
        form = response.context['form']
        self.assertFormError(form, 'name', 'Обязательное поле.')

    # ----- 3. Тесты удаления метки -----
    def test_label_delete(self):
        """Удаление существующей метки"""
        label_to_delete = Label.objects.create(name="Удаляемая метка")
        response = self.client.post(
            reverse('labels:delete', kwargs={'pk': label_to_delete.pk}),
            follow=True
        )
        self.assertContains(response, 'Метка успешно удалена')
        self.assertFalse(Label.objects.filter(pk=label_to_delete.pk).exists())
