from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jgp", upload_to="profile_pics")
    followers = models.ForeignKey(User, on_delete=models.CASCADE,related_name="followers")
    followed = models.ForeignKey(User, on_delete=models.CASCADE,related_name="followed")

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            out = (300, 300)
            img.thumbnail(out)
            img.save(self.image.path)
