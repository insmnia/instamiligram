from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")
    bio = models.TextField(blank=True)
    followers = models.ManyToManyField(User,blank=True,related_name='user_followers',symmetrical=False)
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    following = models.ManyToManyField(User,blank=True,related_name='user_following',symmetrical=False)

    def __str__(self):
        return f"{self.user.username} Profile {self.followers.count()} {self.following.count()}"

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            out = (300, 300)
            img.thumbnail(out)
            img.save(self.image.path)
