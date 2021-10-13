from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from PIL import Image

class Post(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    image = models.ImageField(upload_to="post_pics", default="default.jpg")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author")
    likes = models.ManyToManyField(User,related_name="like",default=None,blank=True)
    likes_count = models.IntegerField(default=0)
    date_posted = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            out = (300, 300)
            img.thumbnail(out)
            img.save(self.image.path)

    def __str__(self):
        return f"{self.title} {self.author}"

    def get_absolute_url(self):
        return reverse("instagram:post-detail", kwargs={"pk": self.pk})
