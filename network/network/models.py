from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    followers = models.ManyToManyField("self", blank=True, related_name="following", symmetrical=False)

    def serialize(self):
        return {
            "id": self.id,
            "followers": self.followers.count(),
        }
    
    def __str__(self):
        return f"{self.username}"


class Post(models.Model):
    subject = models.CharField(max_length=64) 
    content = models.CharField(max_length=280)  
    post_date = models.DateTimeField(default=timezone.now)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posted_posts")
    likes = models.ManyToManyField(User, blank=True, related_name="liked_posts")

    def serialize(self):
        return {
            "id": self.id, 
            "likers": self.likes.count(),
            "content": self.content
        }

    def __str__(self):
        return f"Subject: '{self.subject}' by {self.poster}"
