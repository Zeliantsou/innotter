from rest_framework import serializers

from post.models import Post


class CreatePostSerializer(serializers.ModelSerializer):
    """Serializes post for create view"""

    class Meta:
        model = Post
        fields = (
            'id',
            'page',
            'content',
            'reply_to',
        )


class UpdatePostSerializer(serializers.ModelSerializer):
    """Serializes post for update view"""

    class Meta:
        model = Post
        fields = (
            'id',
            'content',
        )


class RetrievePostSerializer(serializers.ModelSerializer):
    """Serializes post for retrieve view"""
    owner = serializers.SlugRelatedField(slug_field='email', read_only=True)
    page = serializers.SlugRelatedField(slug_field='name', read_only=True)
    reply_to = serializers.SlugRelatedField(slug_field='content', read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'owner',
            'page',
            'content',
            'reply_to',
            'created',
            'updated',
        )


class ListPostSerializer(serializers.ModelSerializer):
    """Serializes post for list view"""
    owner = serializers.SlugRelatedField(slug_field='email', read_only=True)
    page = serializers.SlugRelatedField(slug_field='name', read_only=True)
    reply_to = serializers.SlugRelatedField(slug_field='content', read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'owner',
            'page',
            'content',
            'reply_to',
        )
