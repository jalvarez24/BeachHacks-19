from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey('auth.User',
                               related_name='posts',
                               on_delete=models.CASCADE)
    author_username = models.CharField(max_length=255, default='joe')
    beach_id = models.CharField(max_length=255)
    caption = models.TextField()
    image = models.CharField(max_length=255)
    imageId = models.CharField(max_length=255)
