from rest_framework import serializers

from tag.models import Tag


class CreateTagSerializer(serializers.ModelSerializer):
    """Serializes tag for create view"""

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
        )


class UpdateTagSerializer(serializers.ModelSerializer):
    """Serializes tag for update view"""

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
        )


class RetrieveTagSerializer(serializers.ModelSerializer):
    """Serializes tag for retrieve view"""

    class Meta:
        model = Tag
        fields = (
            'id',
            'owner',
            'name',
        )


class ListTagSerializer(serializers.ModelSerializer):
    """Serializes tag for list view"""

    class Meta:
        model = Tag
        fields = (
            'id',
            'owner',
            'name',
        )
