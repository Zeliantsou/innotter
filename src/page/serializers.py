from rest_framework import serializers

from page.models import Page


class CreatePageSerializer(serializers.ModelSerializer):
    """Serializes page for create view"""
    # owner = serializers.SlugRelatedField(slug_field='email', read_only=True)

    class Meta:
        model = Page
        fields = (
            'id',
            # 'owner'
            'name',
            'description',
            'image',
            'is_private'
        )


class UpdatePageSerializer(serializers.ModelSerializer):
    """Serializes page for create update"""

    class Meta:
        model = Page
        fields = (
            'name',
            'uuid',
            'description',
            'tags',
            'followers',
            'subscriptions',
            'image',
            'is_private',
        )

    # def get_tags(self, obj):
    #     return TagForPageSerializer(obj.owner.tags.all, many=True).data


class RetrievePageSerializer(serializers.ModelSerializer):
    """Serializes page for retrieve view"""
    tags = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    owner = serializers.SlugRelatedField(slug_field='email', read_only=True)
    followers = serializers.SlugRelatedField(slug_field='email', many=True, read_only=True)
    subscriptions = serializers.SlugRelatedField(slug_field='email', many=True, read_only=True)

    class Meta:
        model = Page
        fields = (
            'id',
            'name',
            'uuid',
            'description',
            'tags',
            'owner',
            'followers',
            'subscriptions',
            'image',
            'is_private',
            'unblock_date',
            'is_permanent_blocked'
        )


class ListPageSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='email', read_only=True)

    class Meta:
        model = Page
        fields = (
            'id',
            'name',
            'owner',
            'is_private',
        )
