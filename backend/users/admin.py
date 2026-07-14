from django.contrib import admin

from users import models


@admin.register(models.DeletedUserEmail)
class DeletedUserEmailAdmin(admin.ModelAdmin):
    list_display = ("email", "deleted_at")
    search_fields = ("email",)


@admin.register(models.UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ("user__username", "theme")
    search_fields = ("user__username",)


@admin.register(models.User)
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


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user__username", "avatar", "birth_date", "bio")
    search_fields = ("user__username", "birth_date")


@admin.register(models.Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("user_from__username", "user_to__username", "created_at")
    search_fields = ("user_from__username", "user_to__username")


@admin.register(models.EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ("user__username", "code", "created_at", "expires_at")
    search_fields = ("user__username", "code")
