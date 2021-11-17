import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_name = self.scope['url_route']['kwargs']['username']
        self.chat_group_name = 'chat_%s' % self.chat_name
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        sender = await self.get_user(text_data_json['sender'])
        recipient = await self.get_user(text_data_json['recipient'])
        text = text_data_json['text']
        message = await self.create_message(sender, recipient, text)
        data = {
            'sender': message.sender.username,
            'text': message.text,
            'timestamp': 'just now'
        }
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': data
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def get_user(self, username):
        return User.objects.filter(username=username).first()

    @database_sync_to_async
    def create_message(self, sender, recipient, text):
        msg = Message.objects.create(
            sender=sender,
            recipient=recipient,
            text=text,
        )
        return msg
