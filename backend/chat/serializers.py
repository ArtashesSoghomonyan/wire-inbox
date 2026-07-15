from rest_framework import serializers
from users.models import User
from users.serializers import UserSerializer

from chat.models import (
    DirectConversation,
    DirectMessage,
    GroupConversation,
    GroupMessage,
)


class DirectConversationSerializer(serializers.ModelSerializer):
    participant_1 = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    participant_2 = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    participant_1_details = UserSerializer(source="participant_1", read_only=True)
    participant_2_details = UserSerializer(source="participant_2", read_only=True)

    class Meta:
        model = DirectConversation
        fields = [
            "id",
            "participant_1",
            "participant_2",
            "participant_1_details",
            "participant_2_details",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        participant_1 = attrs.get("participant_1")
        participant_2 = attrs.get("participant_2")

        if participant_1 and participant_2 and participant_1 == participant_2:
            raise serializers.ValidationError(
                "A direct conversation cannot be created with the same user twice."
            )

        return attrs


class GroupConversationSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    participants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
    )
    participant_details = UserSerializer(source="participants", many=True, read_only=True)

    class Meta:
        model = GroupConversation
        fields = [
            "id",
            "name",
            "owner",
            "participants",
            "participant_details",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        participants = validated_data.pop("participants", [])
        conversation = GroupConversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        return conversation


class DirectMessageSerializer(serializers.ModelSerializer):
    conversation = serializers.PrimaryKeyRelatedField(queryset=DirectConversation.objects.all())
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())
    sender_details = UserSerializer(source="sender", read_only=True)

    class Meta:
        model = DirectMessage
        fields = [
            "id",
            "conversation",
            "sender",
            "sender_details",
            "content",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class GroupMessageSerializer(serializers.ModelSerializer):
    conversation = serializers.PrimaryKeyRelatedField(queryset=GroupConversation.objects.all())
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())
    sender_details = UserSerializer(source="sender", read_only=True)

    class Meta:
        model = GroupMessage
        fields = [
            "id",
            "conversation",
            "sender",
            "sender_details",
            "content",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


