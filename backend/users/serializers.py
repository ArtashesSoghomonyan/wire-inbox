import re

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import (
    FORBIDDEN_USERNAMES,
    DeletedUserEmail,
    Follow,
    Profile,
    User,
    UserSettings,
)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    settings = UserSettingsSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "profile",
            "settings",
            "followers_count",
            "following_count",
            "is_verified",
        ]


class SearchUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "profile",
            "followers_count",
            "following_count",
            "is_following",
        ]

    def get_is_following(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Follow.objects.filter(
                user_from=request.user,
                user_to=obj,
            ).exists()
        return False


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True, max_length=50)
    first_name = serializers.CharField(required=True, max_length=30)
    last_name = serializers.CharField(required=True, max_length=30)
    password = serializers.CharField(required=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        elif DeletedUserEmail.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email was deleted. You cannot use this email."
            )
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        if not re.fullmatch(r"[a-z_]+", value):
            raise serializers.ValidationError(
                "Username must be lowercase letters or underscores only"
            )
        if value in FORBIDDEN_USERNAMES:
            raise serializers.ValidationError(
                "Username is not available"
            )
        return value

    def validate_first_name(self, value):
        return value.strip().capitalize()

    def validate_last_name(self, value):
        return value.strip().capitalize()

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"] = serializers.EmailField()
        self.fields.pop("username", None)

    def validate(self, attrs):
        attrs[self.username_field] = attrs.pop("email")
        return super().validate(attrs)


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id", "user_from", "user_to", "created_at"]
        read_only_fields = ["id", "user_from", "created_at"]
