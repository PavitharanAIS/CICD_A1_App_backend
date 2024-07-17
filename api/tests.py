from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.core.management.commands.test import Command as BaseCommand


class Command(BaseCommand):
    def handle(self, *test_labels, **options):
        # Wrap Django's built-in test command to always delete the database if
        # it exists
        options["interactive"] = False
        return super().handle(*test_labels, **options)
class CreateUserViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('register')  # Ensure this name matches your URL pattern name for CreateUserView

    def test_create_user(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_create_user_invalid_data(self):
        data = {
            'username': '',  # Invalid username
            'password': 'testpassword123'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
