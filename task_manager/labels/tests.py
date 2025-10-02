from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.users.models import CustomUser


class LabelCRUDTestWithFixtures(TestCase):
    fixtures = [
        'users.json',
        'statuses.json',
        'labels.json',
        'tasks.json',
    ]

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.get(username='dixon')
        self.client.force_login(self.user)
        self.label = Label.objects.get(pk=1)
        self.labels_url = reverse('labels:labels')
        self.create_url = reverse('labels:create_label')
        self.edit_url = lambda pk: reverse(
            'labels:edit_label', kwargs={'pk': pk}
        )
        self.delete_url = lambda pk: reverse(
            'labels:delete_label', kwargs={'pk': pk}
        )

    def test_label_list_view(self):
        response = self.client.get(self.labels_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.label.name)
        self.assertTemplateUsed(response, 'labels/index.html')

    def test_create_label_view_get(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/create.html')
        self.assertContains(response, 'Имя')

    def test_create_label_view_post_success(self):
        data = {'name': 'New Label'}
        response = self.client.post(self.create_url, data)
        self.assertRedirects(response, self.labels_url)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Метка успешно создана')

        self.assertTrue(Label.objects.filter(name='New Label').exists())

    def test_create_label_view_post_invalid(self):
        data = {'name': ''}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 200)

        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('This field is required.', form.errors['name'][0])

    def test_label_edit_view_get(self):
        response = self.client.get(self.edit_url(self.label.pk))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/edit.html')
        self.assertContains(response, self.label.name)

    def test_label_edit_view_post_success(self):
        data = {'name': 'Updated Label'}
        response = self.client.post(self.edit_url(self.label.id), data)
        self.assertRedirects(response, self.labels_url)

        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated Label')

    def test_label_edit_view_post_invalid(self):
        data = {'name': ''}
        response = self.client.post(self.edit_url(self.label.id), data)
        self.assertEqual(response.status_code, 200)

        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('This field is required.', form.errors['name'][0])

    def test_label_delete_view_get(self):
        response = self.client.get(self.delete_url(self.label.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/label_confirm_delete.html')
        self.assertContains(response, self.label.name)

    def test_label_delete_view_post_success(self):
        deletable_label = Label.objects.get(pk=10)
        response = self.client.post(self.delete_url(deletable_label.id))
        self.assertRedirects(response, self.labels_url)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Метка успешно удалена')

        self.assertFalse(Label.objects.filter(id=deletable_label.id).exists())

    def test_label_delete_view_post_fail_if_used(self):
        used_label = Label.objects.get(pk=1)
        response = self.client.post(self.delete_url(used_label.id))
        self.assertRedirects(response, self.labels_url)

        self.assertTrue(Label.objects.filter(id=used_label.id).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            'Невозможно удалить метку, потому что она используется'
        )

    def test_unauthenticated_access(self):
        self.client.logout()
        urls = [
            self.labels_url,
            self.create_url,
            self.edit_url(self.label.id),
            self.delete_url(self.label.id),
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertRedirects(response, reverse('users:login'))

            response = self.client.post(url)
            self.assertRedirects(response, reverse('users:login'))
