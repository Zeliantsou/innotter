from rest_framework.serializers import ModelSerializer, SlugRelatedField

from post.models import Post


class CreatePostSerializer(ModelSerializer):
    """Serializes post for create view"""

    class Meta:
        model = Post
        fields = (
            'id',
            'page',
            'content',
            'reply_to',
        )


class UpdatePostSerializer(ModelSerializer):
    """Serializes post for update view"""

    class Meta:
        model = Post
        fields = (
            'id',
            'content',
        )


class RetrievePostSerializer(ModelSerializer):
    """Serializes post for retrieve view"""
    owner = SlugRelatedField(slug_field='email', read_only=True)
    page = SlugRelatedField(slug_field='name', read_only=True)
    reply_to = SlugRelatedField(slug_field='content', read_only=True)

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


class ListPostSerializer(ModelSerializer):
    """Serializes post for list view"""
    owner = SlugRelatedField(slug_field='email', read_only=True)
    page = SlugRelatedField(slug_field='name', read_only=True)
    reply_to = SlugRelatedField(slug_field='content', read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'owner',
            'page',
            'content',
            'reply_to',
        )
