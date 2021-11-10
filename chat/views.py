from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render, redirect

# Create your views here.
app_name = 'chat'


class UserChatsView(View):
    def get(self, request, *args, **kwargs):
        u = request.user
        return render(request, "chats/chat-home.html", context={'user': u, 'range': range(5)})
