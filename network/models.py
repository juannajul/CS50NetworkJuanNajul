from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_image = models.ImageField(default='../static/network/img/defaultprofile.jpg', verbose_name='user_photo', upload_to='profile_img')
    pass

class Profile(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

class Post(models.Model):
    content = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    likes = models.ManyToManyField(User, related_name="post_likes", null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "content":self.content,
            "user": self.user.id,
            "likes": [user.username for user in self.likes.all()],
            "created_at": self.created_at.strftime("%b %d %Y, %I:%M %p")
        }

