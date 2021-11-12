from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Message(models.Model):
    sent = models.DateTimeField(default=timezone.now)
    _from = models.OneToOneField(User, on_delete=models.CASCADE)
    _to = models.OneToOneField(User, on_delete=models.CASCADE)


class Dialog(models.Model):
    interlocutor1 = models.OneToOneField(User, on_delete=models.CASCADE)
    interlocutor2 = models.OneToOneField(User, on_delete=models.CASCADE)
    messages = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name='messages')
