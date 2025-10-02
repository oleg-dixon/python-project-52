from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task


class TaskCRUDTestWithFixtures(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.client = Client()

        self.task = Task.objects.get(pk=1)
        self.user = self.task.author
        self.client.force_login(self.user)

        self.status = Status.objects.get(pk=7)
        self.label1 = Label.objects.get(pk=1)
        self.label2 = Label.objects.get(pk=6)

        self.tasks_url = reverse('tasks:tasks')
        self.create_url = reverse('tasks:create_task')
        self.detail_url = lambda pk: reverse(
            'tasks:show_task', kwargs={'pk': pk}
        )
        self.edit_url = lambda pk: reverse(
            'tasks:edit_task', kwargs={'pk': pk}
        )
        self.delete_url = lambda pk: reverse(
            'tasks:delete_task', kwargs={'pk': pk}
        )

    def test_task_list_view(self):
        response = self.client.get(self.tasks_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)
        self.assertTemplateUsed(response, 'tasks/index.html')

    def test_task_create_view_get(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/create.html')
        self.assertIsInstance(response.context['form'], TaskForm)

    def test_task_create_view_post_success(self):
        data = {
            'name': 'New Task',
            'description': 'New Description',
            'status': self.status.id,
            'executor': self.user.id,
            'labels': [self.label1.id, self.label2.id],
        }
        response = self.client.post(self.create_url, data)
        self.assertRedirects(response, self.tasks_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задача успешно создана')
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_task_detail_view(self):
        response = self.client.get(self.detail_url(self.task.pk))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/show_task.html')
        self.assertEqual(response.context['task'], self.task)

    def test_task_edit_view_get(self):
        response = self.client.get(self.edit_url(self.task.pk))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/edit.html')
        self.assertIsInstance(response.context['form'], TaskForm)

    def test_task_edit_view_post_success(self):
        data = {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'status': self.status.id,
            'executor': self.user.id,
            'labels': [self.label1.id],
        }
        response = self.client.post(self.edit_url(self.task.pk), data)
        self.assertRedirects(response, self.tasks_url)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')

    def test_task_delete_view_get(self):
        response = self.client.get(self.delete_url(self.task.pk))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_confirm_delete.html')
        self.assertEqual(response.context['task'], self.task)

    def test_task_delete_view_post(self):
        response = self.client.post(self.delete_url(self.task.pk))
        self.assertRedirects(response, self.tasks_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задача успешно удалена')
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_unauthenticated_access_redirect(self):
        self.client.logout()
        urls = [
            self.tasks_url,
            self.create_url,
            self.detail_url(self.task.pk),
            self.edit_url(self.task.pk),
            self.delete_url(self.task.pk),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertRedirects(response, reverse('users:login'))
            response = self.client.post(url)
            self.assertRedirects(response, reverse('users:login'))
