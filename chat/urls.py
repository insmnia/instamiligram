from .views import (
    UserChatsView,
    DialogChatView
)

from django.urls import path

app_name = "chat"

urlpatterns = [
    path("chats/", UserChatsView.as_view(), name="chats-home"),
    path('chat/<str:username>', DialogChatView.as_view(), name='chats-dialog')
]
