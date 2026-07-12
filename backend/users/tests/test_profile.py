from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import Profile, User


class ProfileTests(APITestCase):
    def test_update_profile(self):
        user = User.objects.create_user(
            email="john@example.com",
            username="john",
            first_name="John",
            last_name="Blacksmith",
            password="password123",
        )

        self.client.post(reverse("users:login"), {
            "email": "john@example.com",
            "password": "password123",
        })

        bio = "new bio test"

        with open("test_data/dog.jpg", "rb") as photo:
            response = self.client.patch(
                reverse("users:profile"),
                {"avatar": photo, "bio": bio},
                format="multipart",
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
