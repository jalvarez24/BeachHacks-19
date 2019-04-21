from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'beachId' 'caption', 'image', 'author', 'date_created', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')