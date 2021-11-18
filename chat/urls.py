from .views import (
    CreateChatView,
    UserChatsView,
    DialogChatView,
)

from django.urls import path

app_name = "chat"

urlpatterns = [
    path("chats/", UserChatsView.as_view(), name="chats-home"),
    path('chat/<str:chatname>', DialogChatView.as_view(), name='chats-dialog'),
    path('chat/create/<str:who>/<str:_with>',CreateChatView.as_view(),name='chats-create')
]
