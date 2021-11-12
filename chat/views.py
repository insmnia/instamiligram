from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render, redirect
from .models import Message
from django.contrib.auth.models import User
# Create your views here.
app_name = 'chat'


class UserChatsView(View):
    def get(self, request, *args, **kwargs):
        msgs = request.user.messages_recieved.order_by('-timestamp').all()
        _messages = []
        senders = []
        for msg in msgs:
            if msg.sender not in senders:
                _messages.append(msg)
                senders.append(msg.sender)
        return render(
            request,
            'chat/chat-home.html',
            context={
                'chat_messages': _messages
            }
        )


class DialogChatView(View):
    def get(self, request, username, *args, **kwargs):
        u_target = User.objects.filter(username=username).first()
        _messages = Message.objects.filter(
            sender=u_target, recipient=request.user).all()
        _messages2 = Message.objects.filter(
            sender=request.user, recipient=u_target).all()
        msgs = _messages | _messages2
        msgs.order_by('-timestamp')
        print(_messages, _messages2)
        return render(request, 'chat/chat-dialog.html', context={
            'target': u_target,
            'msgs': msgs
        })
