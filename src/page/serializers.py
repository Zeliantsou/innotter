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
        read_only_fields = ('followers', 'subscriptions')


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
    """Serializes page for list view"""
    owner = serializers.SlugRelatedField(slug_field='email', read_only=True)

    class Meta:
        model = Page
        fields = (
            'id',
            'name',
            'owner',
            'is_private',
        )


class TemporaryBlockDaySerializer(serializers.ModelSerializer):
    """Serializes unblock date"""
    block_duration_days = serializers.IntegerField()

    class Meta:
        model = Page
        fields = ('block_duration_days', 'unblock_date')

        extra_kwargs = {
            'block_duration_days': {'write_only': True},
            'unblock_date': {'read_only': True},
        }


class DeleteFollowerSerializer(serializers.ModelSerializer):
    """Serializes page for delete follower view"""
    list_ids_removable_follower = serializers.ListSerializer(
        child=serializers.IntegerField(),
        required=False
    )

    class Meta:
        model = Page
        fields = ('id', 'followers', 'list_ids_removable_follower',)

        extra_kwargs = {
            'followers': {'read_only': True},
            'list_ids_removable_follower': {'write_only': True},
        }


class DeleteSubscriptionsSerializer(serializers.ModelSerializer):
    """Serializes page for delete subscriptions view"""
    list_user_ids_refuse_subscribe = serializers.ListSerializer(
        child=serializers.IntegerField(),
        required=False
    )

    class Meta:
        model = Page
        fields = ('id', 'subscriptions', 'list_user_ids_refuse_subscribe',)

        extra_kwargs = {
            'subscriptions': {'read_only': True},
            'list_user_ids_refuse_subscribe': {'write_only': True},
        }
