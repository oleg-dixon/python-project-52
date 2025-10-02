from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.users.models import CustomUser


class StatusCRUDTestWithFixtures(TestCase):
    fixtures = [
        'users.json',
        'statuses.json',
    ]

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.get(username='dixon')
        self.client.force_login(self.user)
        self.status = Status.objects.get(pk=7)
        self.statuses_url = reverse('statuses:statuses')
        self.create_url = reverse('statuses:create_status')
        self.edit_url = lambda pk: reverse(
            'statuses:edit_status', kwargs={'pk': pk}
        )
        self.delete_url = lambda pk: reverse(
            'statuses:delete_status', kwargs={'pk': pk}
        )

    def test_status_list_view(self):
        response = self.client.get(self.statuses_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.status.name)
        self.assertTemplateUsed(response, 'statuses/index.html')

    def test_create_status_view_get(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/create.html')
        self.assertContains(response, 'Имя')

    def test_create_status_view_post_success(self):
        data = {'name': 'New Status'}
        response = self.client.post(self.create_url, data)
        self.assertRedirects(response, self.statuses_url)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Статус успешно создан')

        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_create_status_view_post_invalid(self):
        data = {'name': ''}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 200)

        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('This field is required.', form.errors['name'][0])

    def test_status_edit_view_get(self):
        response = self.client.get(self.edit_url(self.status.pk))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/edit.html')
        self.assertContains(response, self.status.name)

    def test_status_edit_view_post_success(self):
        data = {'name': 'Updated Status'}
        response = self.client.post(self.edit_url(self.status.pk), data)
        self.assertRedirects(response, self.statuses_url)

        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')

    def test_status_edit_view_post_invalid(self):
        data = {'name': ''}
        response = self.client.post(self.edit_url(self.status.pk), data)
        self.assertEqual(response.status_code, 200)

        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('This field is required.', form.errors['name'][0])

    def test_status_delete_view_get(self):
        response = self.client.get(self.delete_url(self.status.pk))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/status_confirm_delete.html')
        self.assertContains(response, self.status.name)

    def test_status_delete_view_post_success(self):
        deletable_status = Status.objects.create(name='Deletable Status')
        response = self.client.post(self.delete_url(deletable_status.pk))
        self.assertRedirects(response, self.statuses_url)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Статус успешно удален')

        self.assertFalse(Status.objects.filter(pk=deletable_status.pk).exists())

    def test_unauthenticated_access(self):
        self.client.logout()
        urls = [
            self.statuses_url,
            self.create_url,
            self.edit_url(self.status.pk),
            self.delete_url(self.status.pk),
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertRedirects(response, reverse('users:login'))

            response = self.client.post(url)
            self.assertRedirects(response, reverse('users:login'))
