from rest_framework import serializers

from like.models import Like


class CreateLikeSerializer(serializers.ModelSerializer):
    """Serializes like for create view"""

    class Meta:
        model = Like
        fields = (
            'id',
            'post',
            'owner',
        )
        extra_kwargs = {
            'owner': {'read_only': True},
        }


class UpdateLikeSerializer(serializers.ModelSerializer):
    """Serializes like for update view"""

    class Meta:
        model = Like
        fields = (
            'post',
        )


class RetrieveLikeSerializer(serializers.ModelSerializer):
    """Serializes like for retrieve view"""
    post = serializers.SlugRelatedField(slug_field='content', read_only=True)

    class Meta:
        model = Like
        fields = (
            'id',
            'post',
        )


class ListLikeSerializer(serializers.ModelSerializer):
    """Serializes like for list view"""
    post = serializers.SlugRelatedField(slug_field='content', read_only=True)

    class Meta:
        model = Like
        fields = (
            'id',
            'post',
        )
