from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import CustomUser


class UserCRUDTestWithFixtures(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.user = CustomUser.objects.get(username='dixon')
        self.other_user = CustomUser.objects.get(username='mary')
        self.client.force_login(self.user)

        self.task = Task.objects.get(pk=1)
        self.status = Status.objects.get(pk=7)
        self.label1 = Label.objects.get(pk=1)
        self.label2 = Label.objects.get(pk=6)

        self.users_list_url = reverse('users:users')
        self.create_user_url = reverse('users:create_user')
        self.login_url = reverse('login')

    def edit_user_url(self, pk):
        return reverse('users:edit_user', kwargs={'pk': pk})

    def delete_user_url(self, pk):
        return reverse('users:delete_user', kwargs={'pk': pk})

    def test_user_registration_success(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        response = self.client.post(self.create_user_url, data)
        self.assertRedirects(response, self.login_url)
        self.assertTrue(CustomUser.objects.filter(username='testuser').exists())

    def test_user_registration_password_mismatch(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser2',
            'password1': 'testpass123',
            'password2': 'wrongpass'
        }
        response = self.client.post(self.create_user_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomUser.objects.filter(username='testuser2').exists())
        self.assertContains(response, 'error', status_code=200)

    def test_user_edit_self(self):
        updated_data = {
            'first_name': 'OlegUpdated',
            'last_name': 'DiukarevUpdated',
            'username': 'dixon',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(
            self.edit_user_url(self.user.pk), data=updated_data
        )
        self.assertRedirects(response, self.users_list_url)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'OlegUpdated')

    def test_user_edit_other_user_forbidden(self):
        updated_data = {
            'first_name': 'MariaUpdated',
            'last_name': 'DiukarevaUpdated',
            'username': 'mary',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(
            self.edit_user_url(self.other_user.pk), data=updated_data
        )
        self.assertIn(response.status_code, [200, 302])
        self.other_user.refresh_from_db()
        self.assertEqual(self.other_user.first_name, 'Maria')
        self.assertEqual(self.other_user.last_name, 'Diukareva')
        if response.status_code == 200:
            self.assertContains(
                response, 'Вы не можете редактировать чужого пользователя'
            )

    def test_user_delete_self_success(self):
        user_without_tasks = CustomUser.objects.get(username='dyidka')
        self.client.force_login(user_without_tasks)
        response = self.client.post(self.delete_user_url(user_without_tasks.pk))
        self.assertRedirects(response, self.users_list_url)
        self.assertFalse(
            CustomUser.objects.filter(pk=user_without_tasks.pk).exists()
        )

    def test_user_delete_self_with_tasks_forbidden(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.delete_user_url(self.user.pk), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/index.html')
        self.assertTrue(CustomUser.objects.filter(pk=self.user.pk).exists())

    def test_user_delete_other_user_forbidden(self):
        response = self.client.post(self.delete_user_url(self.other_user.pk))
        self.assertRedirects(response, self.users_list_url)
        self.assertTrue(CustomUser.objects.filter(pk=self.other_user.pk).exists())

    def test_user_delete_with_tasks_forbidden(self):
        Task.objects.create(
            name='Test Task',
            description='Test Desc',
            author=self.user,
            status_id=7
        )
        response = self.client.post(self.delete_user_url(self.user.pk))
        self.assertRedirects(response, self.users_list_url)
        self.assertTrue(CustomUser.objects.filter(pk=self.user.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(
            'Невозможно удалить пользователя, потому что он используется',
            [str(m) for m in messages]
        )

    def test_unauthenticated_access_redirects(self):
        self.client.logout()
        protected_urls = [
            self.edit_user_url(self.user.pk),
            self.delete_user_url(self.user.pk)
        ]
        for url in protected_urls:
            response = self.client.get(url, follow=False)
            self.assertIn(response.status_code, [200, 302])
            if response.status_code == 302:
                self.assertTrue(response.url.startswith('/users/'))
            else:
                self.assertContains(
                    response,
                    "Только авторизованные пользователи "
                    "могут редактировать или удалять"
                )

            response = self.client.post(url, follow=False)
            self.assertIn(response.status_code, [200, 302])
            if response.status_code == 302:
                self.assertTrue(response.url.startswith('/users/'))
            else:
                self.assertContains(
                    response,
                    "Только авторизованные пользователи "
                    "могут редактировать или удалять"
                )
