from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from users.models import DeletedUserEmail, Profile, User, UserSettings


@receiver(post_save, sender=User)
def create_profile_and_settings(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        UserSettings.objects.create(user=instance)

@receiver(pre_delete, sender=User)
def create_deleted_email_instance(sender, instance, **kwargs):
    DeletedUserEmail.objects.create(email=instance.email)
