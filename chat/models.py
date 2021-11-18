from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.shortcuts import reverse

# TODO сделать общий чат для корректной работы сокетов
class Chat(models.Model):
    name = models.CharField(max_length=100,unique=True,db_index=True)
    # users.username in array
    users = ArrayField(models.CharField(max_length=100),default=list)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('chat:chats-dialog',kwargs={'chatname':self.name})
    

class Message(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    related_chat = models.ForeignKey(Chat,on_delete=models.CASCADE,related_name='messages')

    def __str__(self) -> str:
        return f'{self.sender} sent on {self.timestamp}'