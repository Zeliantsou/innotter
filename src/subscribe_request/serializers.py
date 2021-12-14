from rest_framework.serializers import ModelSerializer, SlugRelatedField

from subscribe_request.models import SubscribeRequest


class CreateSubscribeRequestSerializer(ModelSerializer):
    """Serializes subscribe request for create view"""

    class Meta:
        model = SubscribeRequest
        fields = (
            'id',
            'desired_page',
            'is_accept',
        )


class UpdateSubscribeRequestSerializer(ModelSerializer):
    """Serializes subscribe request for update view"""

    class Meta:
        model = SubscribeRequest
        fields = (
            'desired_page',
            'is_accept',
        )


class RetrieveSubscribeRequestSerializer(ModelSerializer):
    """Serializes subscribe request for retrieve view"""

    class Meta:
        model = SubscribeRequest
        fields = (
            'id',
            'initiator',
            'desired_page',
            'is_accept',
        )


class ListSubscribeRequestSerializer(ModelSerializer):
    """Serializes subscribe request for list view"""

    class Meta:
        model = SubscribeRequest
        fields = (
            'id',
            'initiator',
            'desired_page',
            'is_accept',
        )
