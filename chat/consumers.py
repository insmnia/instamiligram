import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

from chat.models import Chat, Message



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_name = self.scope['url_route']['kwargs']['chatname']
        self.chat_group_name = 'chat_%s' % self.chat_name
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        print(f'New connection on layer {self.chat_name} with gn {self.chat_group_name}')
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        sender = await self.get_user(text_data_json['sender'])
        text = text_data_json['text']
        chatname = text_data_json['chatname']
        new_msg = await self.create_msg(sender,text,chatname)
        data = {
            'sender':new_msg.sender.username,
            'text':new_msg.text,
            'timestamp':'just now'
        }
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type':'new_message',
                'message':data
            }
        )
        
    async def new_message(self,event):
        msg = event['message']
        await self.send(text_data=json.dumps({
            'message':msg
        }))


    @database_sync_to_async
    def get_user(self,username):
        return User.objects.filter(username=username).first()

    # @database_sync_to_async
    # def get_chat(self,chatname):
    #     return Chat.objects.filter(name=chatname).first()

    @database_sync_to_async
    def create_msg(self,sender,text,chatname):
        msg = Message.objects.create(
            sender=sender,
            text=text,
            related_chat = Chat.objects.filter(name=chatname).first()
        )
        return msg
    
