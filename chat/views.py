from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render, redirect
from .models import Message
# Create your views here.
app_name = 'chat'


class UserChatsView(View):
    def get(self, request, *args, **kwargs):
        _messages = request.user.messages_recieved.all()
        return render(
            request,
            'chat/chat-home.html',
            context={
                'chat_messages':_messages
            }
        )
