# from django.contrib.auth import get_user_model
# from django.test import TestCase
# from django.urls import reverse
# from .models import Task


# class AuthTestCase(TestCase):
#     """Базовый класс для тестов с авторизованным пользователем"""

#     def setUp(self):
#         self.user = get_user_model().objects.create_user(
#             username="testuser",
#             password="password123"
#         )
#         self.client.login(username="testuser", password="password123")


# class TasksTest(AuthTestCase):
#     fixtures = ["tasks.json"]

#     # ----- 1. Тесты обновления задачи -----
#     def test_update_task(self):
#         """Проверка успешного обновления задачи"""
#         update_url = reverse('tasks:update', kwargs={'pk': 1})
#         response = self.client.post(
#             update_url,
#             data={
#                 "name": "Убери посуду",
#                 "description": "Всю",
#                 "task": 'null',
#                 "author": 2,
#                 "executor": 2,
#             },
#             follow=True
#         )
#         task = Task.objects.get(pk=1)
#         self.assertEqual(task.name, "В работе")
#         self.assertContains(response, "<td>В работе</td>", html=True)
#         self.assertNotContains(response, "<td>Уже в работе</td>", html=True)

#     def test_update_task_unique_validation(self):
#         """Нельзя установить существующее название статуса"""
#         update_url = reverse('tasks:update', kwargs={'pk': 1})
#         response = self.client.post(
#             update_url,
#             data={"name": "На рассмотрении"}
#         )
#         form = response.context['form']
#         self.assertFormError(
#             form,
#             'name',
#             'Статус с таким названием уже существует.'
#         )

#     def test_update_task_empty(self):
#         """Нельзя оставить пустое название статуса"""
#         update_url = reverse('tasks:update', kwargs={'pk': 1})
#         response = self.client.post(update_url, data={"name": ""})
#         form = response.context['form']
#         self.assertFormError(form, 'name', 'Обязательное поле.')

#     # ----- 2. Тесты создания статуса -----
#     def test_create_task_success(self):
#         """Создание нового статуса через форму"""
#         create_url = reverse('tasks:create')
#         response = self.client.post(
#             create_url,
#             data={"name": "В продакшен"},
#             follow=True
#         )
#         task = task.objects.get(name="В продакшен")
#         self.assertEqual(task.name, "В продакшен")
#         self.assertContains(response, "Статус успешно создан")

#     def test_create_task_unique_validation(self):
#         """Нельзя создать статус с уже существующим названием"""
#         create_url = reverse('tasks:create')
#         response = self.client.post(
#             create_url,
#             data={"name": "На рассмотрении"}
#         )
#         form = response.context['form']
#         self.assertFormError(
#             form,
#             'name',
#             'Статус с таким названием уже существует.'
#         )

#     def test_task_creation_form_error(self):
#         """Отправка пустой формы при создании статуса"""
#         response = self.client.post(reverse('tasks:create'), {}, follow=True)
#         form = response.context['form']
#         self.assertFormError(form, 'name', 'Обязательное поле.')

#     # ----- 3. Тесты удаления статуса -----
#     def test_task_delete(self):
#         """Удаление существующего статуса"""
#         task_to_delete = task.objects.create(name="Удаляемый статус")
#         response = self.client.post(
#             reverse('tasks:delete', kwargs={'pk': task_to_delete.pk}),
#             follow=True
#         )
#         self.assertContains(response, 'Статус успешно удален')
#         self.assertFalse(task.objects.filter(pk=task_to_delete.pk).exists())
