from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)

from subscribe_request.models import SubscribeRequest
from subscribe_request.serializers import (
    CreateSubscribeRequestSerializer,
    RetrieveSubscribeRequestSerializer,
    UpdateSubscribeRequestSerializer,
    ListSubscribeRequestSerializer
)


class SubscribeRequestViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    GenericViewSet
):
    queryset = SubscribeRequest.objects.all()
    serializer_classes = {
            'create': CreateSubscribeRequestSerializer,
            'update': UpdateSubscribeRequestSerializer,
            'partial_update': UpdateSubscribeRequestSerializer,
            'retrieve': RetrieveSubscribeRequestSerializer,
            'list': ListSubscribeRequestSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)
