from django.urls import re_path, path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('wschat/<str:chatname>/', ChatConsumer.as_asgi())
]
