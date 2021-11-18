from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Chat, Message
from django.http import HttpResponseRedirect
# Create your views here.
app_name = 'chat'


class UserChatsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        chats = Chat.objects.filter(users__contains=[request.user.username]).all()
        return render(
            request,
            'chat/chat-home.html',
            context={
                'chats':chats,
                'users':request.user.profile.following.all()
            }
        )


class DialogChatView(LoginRequiredMixin, View):
    def get(self, request, chatname, *args, **kwargs):
        msgs = Chat.objects.filter(name=chatname).first().messages.all().order_by('-timestamp')
        return render(request, 'chat/chat-dialog.html', context={
            'msgs':msgs,
            'chatname':chatname
        })

class CreateChatView(LoginRequiredMixin,View):
    def get(self,request,who,_with):
        print(f'Creating chat with {who} and {_with}')
        c = Chat.objects.filter(name=who+_with).first()
        if not c:
            c = Chat.objects.create(
                name=who+'-'+_with,
                users=[who,_with]
            )
        return HttpResponseRedirect(c.get_absolute_url())
