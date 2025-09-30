from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.statuses.models import Status


class StatusCRUDIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_full_crud_cycle(self):
        create_url = reverse('statuses') + 'create/'
        response = self.client.post(create_url, {'name': 'Test Status'})
        self.assertEqual(response.status_code, 302)
        status = Status.objects.first()
        self.assertEqual(status.name, "Test Status")

        list_url = reverse('statuses')
        response = self.client.get(list_url)
        self.assertContains(response, "Test Status")

        update_url = reverse('edit_status', kwargs={'status_id': status.id})
        response = self.client.post(update_url, {'name': 'Updated Status'})
        self.assertEqual(response.status_code, 302)
        status.refresh_from_db()
        self.assertEqual(status.name, "Updated Status")

        delete_url = reverse('delete_status', kwargs={'status_id': status.id})
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.count(), 0)