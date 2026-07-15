from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from users.permissions import IsVerified

from chat.models import (
    DirectConversation,
    DirectMessage,
    GroupConversation,
    GroupMessage,
)
from chat.serializers import (
    DirectConversationSerializer,
    DirectMessageSerializer,
    GroupConversationSerializer,
    GroupMessageSerializer,
)


class MyConversations(APIView):
    permission_classes = [IsVerified]

    def get(self, request, *args, **kwargs):
        user = request.user

        direct_conversations = DirectConversation.objects.filter(
            Q(participant_1=user) | Q(participant_2=user)
        ).distinct().order_by("-created_at")

        group_conversations = GroupConversation.objects.filter(participants=user).distinct().order_by(
            "-created_at"
        )

        return Response(
            {
                "direct_conversations": DirectConversationSerializer(
                    direct_conversations,
                    many=True,
                    context={"request": request},
                ).data,
                "group_conversations": GroupConversationSerializer(
                    group_conversations,
                    many=True,
                    context={"request": request},
                ).data,
            }
        )


class DirectConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsVerified]
    serializer_class = DirectConversationSerializer

    def get_queryset(self):
        user = self.request.user
        return DirectConversation.objects.filter(
            Q(participant_1=user) | Q(participant_2=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save()


class GroupConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsVerified]
    serializer_class = GroupConversationSerializer

    def get_queryset(self):
        user = self.request.user
        return GroupConversation.objects.filter(participants=user).distinct()

    def perform_create(self, serializer):
        serializer.save()



class DirectMessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsVerified]
    serializer_class = DirectMessageSerializer

    def get_queryset(self):
        user = self.request.user
        return DirectMessage.objects.filter(
            conversation__in=DirectConversation.objects.filter(
                Q(participant_1=user) | Q(participant_2=user)
            ).distinct()
        ).order_by("created_at")

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class GroupMessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsVerified]
    serializer_class = GroupMessageSerializer

    def get_queryset(self):
        user = self.request.user
        return GroupMessage.objects.filter(
            conversation__in=GroupConversation.objects.filter(participants=user).distinct()
        ).order_by("created_at")

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
