import os

from django.conf import settings
from django.core.files.images import ImageFile
from django.core.management import BaseCommand

from users.models import Profile, User


class Command(BaseCommand):
    help = "This command creates dummy users."

    def handle(self, *args, **options):
        users = [
            {
                "email": "johnsmith@gmail.com",
                "username": "johnsmith",
                "first_name": "John",
                "last_name": "Smith",
                "password": "testpassword1234!",
                "avatar": "dog.jpg",
                "bio": "Hello my name is John Smith",
            },
            {
                "email": "alex.jones@aol.com",
                "username": "alex",
                "first_name": "Alex",
                "last_name": "Jones",
                "password": "testpassword1234!",
                "avatar": "patrick.jpeg",
                "bio": "Hello my name is Alex Jones",
            },
            {
                "email": "jane_blacksmith@live.com",
                "username": "jane",
                "first_name": "Jane",
                "last_name": "Blacksmith",
                "password": "testpassword1234!",
                "avatar": "cat.jpg",
                "bio": "Hello I am Jane, save me from choking Walter",
            },
        ]

        test_data_dir = os.path.join(settings.BASE_DIR, "test_data")

        for user_data in users:
            user, created = User.objects.get_or_create(
                email=user_data["email"],
                defaults={
                    "username": user_data["username"],
                    "first_name": user_data["first_name"],
                    "last_name": user_data["last_name"],
                },
            )

            if created:
                user.set_password(user_data["password"])
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user {user.email}"))
            else:
                self.stdout.write(self.style.WARNING(f"User {user.email} already exists"))

            profile, _ = Profile.objects.get_or_create(user=user)
            profile.bio = user_data["bio"]

            avatar_path = os.path.join(test_data_dir, user_data["avatar"])
            if os.path.exists(avatar_path):
                with open(avatar_path, "rb") as avatar_file:
                    profile.avatar.save(user_data["avatar"], ImageFile(avatar_file), save=False)
            else:
                self.stdout.write(self.style.WARNING(f"Avatar file not found: {avatar_path}"))

            profile.save()
            self.stdout.write(self.style.SUCCESS(f"Updated profile for {user.username}"))
