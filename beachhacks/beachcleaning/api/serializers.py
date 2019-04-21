from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Post
        fields = ('id', 'beach_id', 'caption', 'image', 'author',
                  'author_username')


class TokenSerializer(serializers.Serializer):
    # Serializes token data
    token = serializers.CharField(max_length=255)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined')
