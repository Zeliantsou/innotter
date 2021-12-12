from rest_framework.serializers import ModelSerializer

from tag.models import Tag


class CreateTagSerializer(ModelSerializer):
    """Serializes tag for create view"""

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
        )


class UpdateTagSerializer(ModelSerializer):
    """Serializes tag for update view"""

    class Meta:
        model = Tag
        fields = (
            'name',
        )


class RetrieveTagSerializer(ModelSerializer):
    """Serializes tag for retrieve view"""

    class Meta:
        model = Tag
        fields = (
            'id',
            'owner',
            'name',
        )


class ListTagSerializer(ModelSerializer):
    """Serializes tag for list view"""

    class Meta:
        model = Tag
        fields = (
            'id',
            'owner',
            'name',
        )
