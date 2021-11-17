from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Chat, Message
# Create your views here.
app_name = 'chat'


class UserChatsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        chats = Chat.objects.filter(users__contains=[request.user.username]).all()
        return render(
            request,
            'chat/chat-home.html',
            context={
                'chats':chats
            }
        )


class DialogChatView(LoginRequiredMixin, View):
    def get(self, request, chatname, *args, **kwargs):
        msgs = Chat.objects.filter(name=chatname).first().messages.all().order_by('-timestamp')
        return render(request, 'chat/chat-dialog.html', context={
            'msgs':msgs,
            'chatname':chatname
        })
