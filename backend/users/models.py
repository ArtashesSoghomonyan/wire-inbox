import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from PIL import Image

FORBIDDEN_USERNAMES = [
    "signup",
    "profile",
    "settings",
]

ALLOWED_EMAIL_DOMAINS = [
    "gmail.com",
    "outlook.com",
    "hotmail.com",
    "live.com",
    "msn.com",
    "yahoo.com",
    "icloud.com",
    "me.com",
    "mac.com",
    "aol.com",
    "proton.me",
    "protonmail.com",
    "gmx.com",
    "gmx.de",
    "mail.com",
    "yandex.com",
    "yandex.ru",
    "zoho.com",
    "fastmail.com",
    "tuta.com",
    "tutanota.com",
    "hey.com",
    "qq.com",
    "163.com",
    "126.com",
    "sina.com",
    "naver.com",
    "daum.net",
    "hanmail.net",
    "rediffmail.com",
    "orange.fr",
    "free.fr",
    "laposte.net",
    "comcast.net",
    "verizon.net",
    "att.net",
    "bellsouth.net",
    "cox.net",
    "btinternet.com",
    "virginmedia.com",
    "shaw.ca",
    "rogers.com",
    "telus.net",
    "optonline.net",
    "earthlink.net",
    "web.de",
    "libero.it",
    "seznam.cz",
    "mail.ru",
]


def validate_username_not_forbidden(value):
    if value.lower() in FORBIDDEN_USERNAMES:
        raise ValidationError(
            "This username is not allowed.",
            code="forbidden_username",
        )

def allowed_email_domain_validator(value: str):
    if value.split("@")[1] not in ALLOWED_EMAIL_DOMAINS:
        raise ValidationError(
            "This email domain is not supported."
        )

def deleted_email_validator(value: str):
    if DeletedUserEmail.objects.filter(email=value).exists():
        raise ValidationError(
            "This email cannot be used, because it has been used before."
        )


class DeletedUserEmail(models.Model):
    email = models.EmailField(unique=True)
    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class UserManager(BaseUserManager["User"]):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError("Email is required.")
        if not username:
            raise ValueError("Username is required.")
        if not first_name:
            raise ValueError("First name is required.")
        if not last_name:
            raise ValueError("Last name is required.")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password=None):
        user = self.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(regex=r"^[a-z_]+$"),
            validate_username_not_forbidden
        ],
        unique=True,
        db_index=True,
    )
    email = models.EmailField(
        validators=[deleted_email_validator, allowed_email_domain_validator],
        unique=True,
        db_index=True,
    )
    first_name = models.CharField(max_length=30, db_index=True)
    last_name = models.CharField(max_length=30, db_index=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    following = models.ManyToManyField(
        "self",
        through="Follow",
        symmetrical=False,
        through_fields=("user_from", "user_to"),
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    @property
    def followers_count(self):
        return self.follower_set.count()

    @property
    def following_count(self):
        return self.following_set.count()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class UserSettings(models.Model):
    class ThemeChoices(models.TextChoices):
        SYSTEM_LIGHT = "light"
        SYSTEM_DARK = "dark"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="settings",
    )
    theme = models.CharField(
        max_length=20,
        choices=ThemeChoices,
        default=ThemeChoices.SYSTEM_LIGHT,
    )

    def __str__(self):
        return f"{self.user.username}'s settings"



def avatar_upload_path(instance, filename):
    extension = filename.split(".")[-1]
    return f"avatars/{uuid.uuid4()}.{extension}"


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    avatar = models.ImageField(
        upload_to=avatar_upload_path, null=True, blank=True,
    )
    birth_date = models.DateField(blank=True, null=True)
    bio = models.TextField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.user.username}'s profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.avatar:
            return

        try:
            avatar = Image.open(self.avatar.path)
        except (ValueError, FileNotFoundError, OSError):
            return

        if avatar.height > 400 or avatar.width > 400:
            output_size = (400, 400)
            avatar.thumbnail(output_size)
            avatar.save(self.avatar.path)


class Follow(models.Model):
    user_from = models.ForeignKey(User, related_name="following_set", on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name="follower_set", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user_from", "user_to")


class EmailVerification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="email_verification",
    )

    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ["-created_at"]

    @property
    def expired(self):
        return timezone.now() > self.expires_at
