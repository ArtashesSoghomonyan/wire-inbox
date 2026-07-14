from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class AuthTests(APITestCase):
    def setUp(self):
        self.email = "test@example.com"
        self.username = "testuser"
        self.password = "testpassword123"
        self.first_name = "John"
        self.last_name = "Smith"

        self.user = User.objects.create_user(
            email=self.email,
            username=self.username,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
        )

    def test_login_endpoint(self):
        data = {
            "email": self.email,
            "password": self.password,
        }
        response = self.client.post(reverse("users:login"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_wrong_data(self):
        wrong_data = {
            "email": "wrong@example.com",
            "password": "password123",
        }
        response = self.client.post(reverse("users:login"), wrong_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_endpoint(self):
        data = {
            "email": self.email,
            "password": self.password,
        }
        self.client.post(reverse("users:login"), data)
        response_logout = self.client.post(reverse("users:logout"))
        self.assertEqual(response_logout.status_code, status.HTTP_200_OK)
        # Checking so that /me returns 401 status code
        response_me = self.client.get(reverse("users:me"))
        self.assertEqual(response_me.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_logout_unauthorized(self):
        response_logout = self.client.post(reverse("users:logout"))
        self.assertEqual(response_logout.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_success(self):
        data = {
            "email": self.email,
            "password": self.password,
        }
        self.client.post(reverse("users:login"), data)
        response_me = self.client.get(reverse("users:me"))
        self.assertEqual(response_me.status_code, status.HTTP_200_OK)

        self.assertEqual(response_me.data["username"], self.username)
        self.assertEqual(response_me.data["first_name"], self.first_name)
        self.assertEqual(response_me.data["last_name"], self.last_name)

    def test_me_fail(self):
        response_me = self.client.get(reverse("users:me"))
        self.assertEqual(response_me.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_verify_account_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("users:verify-account"),
            {"code": self.user.email_verification.code},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)

    def test_verify_account_wrong_code(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("users:verify-account"),
            {"code": "000000"},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_verified)
