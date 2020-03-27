from rest_framework import serializers

from .models import Post, Like


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('id', 'user', 'updated_at')


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'content', 'author', 'edited', 'created_at')

    def create(self, validated_data):
        validated_data['author'] = self.context.get('request').user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.edited = True
        return super().update(instance, validated_data)
