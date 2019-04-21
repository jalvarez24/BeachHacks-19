from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'beachId'
                  'caption', 'image', 'author', 'date_created',
                  'date_modified')
        read_only_fields = ('date_created', 'date_modified')


class TokenSerializer(serializers.Serializer):
    # Serializes token data
    token = serializers.CharField(max_length=255)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined')
