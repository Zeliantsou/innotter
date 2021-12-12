from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)

from tag.models import Tag
from tag.serializers import (
    CreateTagSerializer,
    RetrieveTagSerializer,
    UpdateTagSerializer,
    ListTagSerializer
)


class TagViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    GenericViewSet
):
    queryset = Tag.objects.all()
    serializer_classes = {
            'create': CreateTagSerializer,
            'update': UpdateTagSerializer,
            'partial_update': UpdateTagSerializer,
            'retrieve': RetrieveTagSerializer,
            'list': ListTagSerializer,
    }

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.custom_user
        tag = Tag.objects.create(**serializer.validated_data)
        serializer.validated_data['id'] = tag.id

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)
