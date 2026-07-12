from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RegistrationTests(APITestCase):
    def setUp(self):
        self.email = "testuser@example.com"
        self.username = "testuser"
        self.first_name = "Test"
        self.last_name = "Smith"
        self.password = "testpassword123"
        self.birth_date = "2000-01-15"

    def test_register_success(self):
        response = self.client.post(reverse("users:register"), {
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password": self.password,
            "birth_date": self.birth_date,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["username"], self.username)

    def test_register_fail(self):
        response = self.client.post(reverse("users:register"), {
            "email": self.email,
            "username": "Username", # testing the validation
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password": self.password,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
