from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.mixins import LanguageMixin

from .models import Task


class AuthTestCase(TestCase):
    """Базовый класс для тестов с авторизованным пользователем."""

    def setUp(self):
        self.user = get_user_model().objects.get(pk=2)
        self.client.force_login(self.user)


class TasksTest(LanguageMixin, AuthTestCase):
    fixtures = ["labels.json", "users.json", "statuses.json", "tasks.json"]

    # ----- 1. Тест создания задачи -----
    def test_create_task(self):
        status = Status.objects.first()
        author = get_user_model().objects.get(pk=2)
        executor = get_user_model().objects.get(pk=2)
        label = Label.objects.first()

        response = self.client.post(
            reverse('tasks:create'),
            data={
                "name": "Новая задача",
                "description": "Описание задачи",
                "author": author.pk,
                "status": status.pk,
                "executor": executor.pk,
                "labels": [label.pk],
            },
            follow=True
        )

        task = Task.objects.get(name="Новая задача")
        self.assertEqual(task.author, author)
        self.assertEqual(task.executor, executor)
        self.assertEqual(task.status, status)
        self.assertIn(label, task.labels.all())
        self.assertContains(response, "Новая задача")
        self.assertContains(response, "Задача успешно создана")

    # ----- 2. Тест обновления задачи -----
    def test_update_task(self):
        task = Task.objects.get(pk=1)
        status = Status.objects.get(pk=1)
        author = get_user_model().objects.get(pk=2)
        executor = get_user_model().objects.get(pk=2)
        label = Label.objects.first()

        response = self.client.post(
            reverse('tasks:update', kwargs={'pk': task.pk}),
            data={
                "name": "Убери посуду",
                "description": "Всю",
                "author": author.pk,
                "status": status.pk,
                "executor": executor.pk,
                "labels": [label.pk],
            },
            follow=True
        )

        task.refresh_from_db()
        self.assertEqual(task.name, "Убери посуду")
        self.assertEqual(task.status, status)
        self.assertIn(label, task.labels.all())
        self.assertContains(response, "<td>Убери посуду</td>", html=True)

    # ----- 3. Тест удаления задачи -----
    def test_delete_task(self):
        task = Task.objects.get(pk=1)

        response = self.client.post(
            reverse('tasks:delete', kwargs={'pk': task.pk}),
            follow=True
        )

        self.assertFalse(Task.objects.filter(pk=task.pk).exists())
        self.assertContains(response, "Задача успешно удалена")

    # ----- 4. Тест фильтрации по статусу -----
    def test_task_filter_by_status(self):
        status = Status.objects.get(pk=1)
        response = self.client.get(reverse('tasks:index'), data={"status": status.pk})
        tasks = response.context['tasks']
        self.assertTrue(all(task.status == status for task in tasks))

    # ----- 5. Тест фильтрации по исполнителю -----
    def test_task_filter_by_executor(self):
        executor = get_user_model().objects.get(pk=2)
        response = self.client.get(reverse('tasks:index'), data={"executor": executor.pk})
        tasks = response.context['tasks']
        self.assertTrue(all(task.executor == executor for task in tasks))

    # ----- 6. Тест фильтрации по автору -----
    def test_task_filter_by_author(self):
        author = get_user_model().objects.get(pk=2)
        response = self.client.get(reverse('tasks:index'), data={"author": author.pk})
        tasks = response.context['tasks']
        self.assertTrue(all(task.author == author for task in tasks))

    # ----- 7. Тест фильтрации по меткам -----
    def test_task_filter_by_labels(self):
        label = Label.objects.get(pk=1)
        response = self.client.get(reverse('tasks:index'), data={"labels": [label.pk]})
        tasks = response.context['tasks']
        self.assertTrue(any(label in task.labels.all() for task in tasks))

    # ----- 8. Тест фильтрации своих задач -----
    def test_task_filter_self_tasks(self):
        response = self.client.get(reverse('tasks:index'), data={"self_tasks": True})
        tasks = response.context['tasks']
        self.assertTrue(all(task.author == self.user for task in tasks))

    # ----- 9. Тест запрета редактирования чужой задачи -----
    def test_update_other_user_task(self):
        task = Task.objects.get(pk=2)
        status = Status.objects.first()
        executor = get_user_model().objects.get(pk=3)
        author = get_user_model().objects.get(pk=2)

        response = self.client.post(
            reverse('tasks:update', kwargs={'pk': task.pk}),
            data={
                "name": "Попытка изменить чужое",
                "description": "Описание",
                "status": status.pk,
                "executor": executor.pk,
                "author": author.pk,
            },
            follow=True
        )

        task.refresh_from_db()
        self.assertNotEqual(task.name, "Попытка изменить чужое")
        self.assertContains(response, "У вас нет прав для удаления этой задачи.")

    # ----- 10. Тест запрета удаления чужой задачи -----
    def test_delete_other_user_task(self):
        task = Task.objects.get(pk=2)

        response = self.client.post(
            reverse('tasks:delete', kwargs={'pk': task.pk}),
            follow=True
        )

        self.assertTrue(Task.objects.filter(pk=task.pk).exists())
        self.assertContains(response, "У вас нет прав для удаления этой задачи.")

    # ----- 11. Тест просмотра списка задач -----
    def test_task_list_view(self):
        response = self.client.get(reverse('tasks:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<table")
        self.assertTrue(len(response.context['tasks']) > 0)

    # ----- 12. Тест создания задачи с пустыми полями (валидация) -----
    def test_create_task_empty_fields(self):
        response = self.client.post(
            reverse('tasks:create'),
            data={
                "name": "",
                "description": "",
                "status": "",
                "executor": "",
                "labels": [],
            },
            follow=True
        )
        form = response.context["form"]
        self.assertFormError(form, "name", "Обязательное поле.")
        self.assertFormError(form, "status", "Обязательное поле.")
        self.assertNotIn("executor", form.errors)
