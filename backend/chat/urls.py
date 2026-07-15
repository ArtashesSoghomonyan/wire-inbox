from django.urls import path

from chat.views import MyConversations

urlpatterns = [
    path("conversations/", MyConversations.as_view(), name="my_conversations"),
]
