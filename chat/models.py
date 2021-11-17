from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
# TODO сделать общий чат для корректной работы сокетов


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='messages_sent',)
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='messages_recieved',)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    text = models.TextField()

    def __str__(self):
        return f'{self.sender} sended to {self.recipient} at {self.timestamp}'
