from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    beachId = models.IntegerField()
    caption = models.TextField()
    image = models.CharField(max_length=255)
    rating = models.IntegerField()
