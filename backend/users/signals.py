import random
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone

from users.emails import verification_email_html
from users.models import (
    DeletedUserEmail,
    EmailVerification,
    Profile,
    User,
    UserSettings,
)


@receiver(post_save, sender=User)
def create_profile_and_settings(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        UserSettings.objects.create(user=instance)

        # Email verification
        verification_code = f"{random.randint(0, 999999):06d}"

        EmailVerification.objects.create(
            user=instance,
            code=verification_code,
            expires_at=timezone.now() + timedelta(minutes=20),
        )

        email_title, email_content = verification_email_html(instance.username, verification_code)

        send_mail(
            subject=email_title,
            message=email_content,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.email],
        )

@receiver(pre_delete, sender=User)
def create_deleted_email_instance(sender, instance, **kwargs):
    if instance.is_verified:
        DeletedUserEmail.objects.create(email=instance.email)

