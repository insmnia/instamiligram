from .views import (
    UserChatsView
)

from django.urls import path

app_name = "chat"

urlpatterns = [
    path("chats/", UserChatsView.as_view(), name="chats-home"),
]
