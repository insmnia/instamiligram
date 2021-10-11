from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author")
    likes = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="likes")
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} {self.author} {self.likes}"

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
