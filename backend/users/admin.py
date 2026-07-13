from django.contrib import admin

from .models import Profile, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "date_joined",
        "last_login",
        "is_admin",
        "is_active",
        "is_staff",
        "is_superuser",
        "is_verified",
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "avatar",
        "bio",
        "birth_date",
    )
