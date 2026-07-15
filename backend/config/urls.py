from chat.views import (
    DirectConversationViewSet,
    DirectMessageViewSet,
    GroupConversationViewSet,
    GroupMessageViewSet,
)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import status
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView

router = DefaultRouter()
router.register("direct-conversations", DirectConversationViewSet, basename="direct-conversations")
router.register("group-conversations", GroupConversationViewSet, basename="group-conversations")
router.register("direct-messages", DirectMessageViewSet, basename="direct-messages")
router.register("group-messages", GroupMessageViewSet, basename="group-messages")

class APIHealthView(APIView):
    def get(self, request):
        return Response({
            "message": "OK",
        }, status=status.HTTP_200_OK)

urlpatterns = [
    path("api/chat", include(("chat.urls", "chat"))),
    path("api/health/", APIHealthView.as_view(), name="health"),
    path("api/users/", include(("users.urls", "users"))),
]

if settings.DEBUG:
    urlpatterns.append(path("admin/", admin.site.urls))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns.append(path(f"{settings.ADMIN_PATH}/", admin.site.urls))
