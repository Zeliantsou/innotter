from rest_framework import serializers

from subscribe_request.models import SubscribeRequest


class CreateSubscribeRequestSerializer(serializers.ModelSerializer):
    """Serializes subscribe request for create view"""

    class Meta:
        model = SubscribeRequest
        fields = (
            'initiator_page',
            'desired_page',
        )


class UpdateSubscribeRequestSerializer(serializers.ModelSerializer):
    """Serializes subscribe request for update view"""

    class Meta:
        model = SubscribeRequest
        fields = (
            'is_accept',
        )


class RetrieveSubscribeRequestSerializer(serializers.ModelSerializer):
    """Serializes subscribe request for retrieve view"""

    class Meta:
        model = SubscribeRequest
        fields = (
            'id',
            'initiator',
            'desired_page',
            'is_accept',
        )


class ListSubscribeRequestSerializer(serializers.ModelSerializer):
    """Serializes subscribe request for list view"""

    class Meta:
        model = SubscribeRequest
        fields = (
            'id',
            'initiator',
            'desired_page',
            'is_accept',
        )
