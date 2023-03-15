from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    posted_by = models.ForeignKey(User, related_name='posted_by', on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    body = models.CharField( max_length=100)
    like = models.ManyToManyField(User, related_name='liked_by', blank=True)
    likes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True, blank=True)
    about = models.TextField(blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    age = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.username