from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=20)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name="author")
    likes = models.ForeignKey(User, on_delete=models.CASCADE,related_name="likes")

    def __str__(self):
        return f"{self.title} {self.author} {self.likes}"
