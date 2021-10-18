from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.postgres.fields import ArrayField


class Like(models.Model):
    user = models.ForeignKey(User, related_name="likes",
                             on_delete=models.CASCADE)
    # Generic foreign key
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')

class Post(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    image = models.ImageField(upload_to="post_pics", default="default.jpg")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author")
    likes = GenericRelation(Like)
    date_posted = models.DateTimeField(default=timezone.now)
    tags = ArrayField(models.CharField(max_length=40),default=list)

    def __str__(self):
        return f"Post by {self.author}"
    
    @property
    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse("instagram:post-detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    likes = GenericRelation(Like)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"Comment on {self.post}"

    @property
    def total_likes(self):
        return self.likes.count()