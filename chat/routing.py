from django.urls import re_path, path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('chat/<str:username>', ChatConsumer.as_asgi())
]