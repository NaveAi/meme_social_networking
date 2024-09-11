from rest_framework import serializers
from .models import Meme, Comment

class MemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meme
        fields = ['id', 'title', 'image', 'creator', 'created_at', 'likes']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'meme', 'user', 'content', 'created_at']