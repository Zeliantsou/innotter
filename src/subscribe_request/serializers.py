from rest_framework.serializers import ModelSerializer, ListSerializer, IntegerField

from subscribe_request.models import SubscribeRequest


class CreateSubscribeRequestSerializer(ModelSerializer):
    """Serializes subscribe request for create view"""

    class Meta:
        model = SubscribeRequest
        fields = (
            'initiator_page',
            'desired_page',
        )


class UpdateSubscribeRequestSerializer(ModelSerializer):
    """Serializes subscribe request for update view"""

    class Meta:
        model = SubscribeRequest
        fields = (
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


# class AcceptSeveralRequestsSerializer(ModelSerializer):
#     """Serializes subscribe requests for accept view"""
#     list_ids_accepted_requests = ListSerializer(
#         child=IntegerField(),
#         required=False,
#     )
#
#     class Meta:
#         model = SubscribeRequest
#         fields = (
#             'id',
#             'is_accept',
#         )
#
#     extra_kwargs = {
#         'list_ids_accepted_requests': {'write_only': True},
#     }
