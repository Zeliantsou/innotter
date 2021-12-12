from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)

from like.models import Like
from like.serializers import (
    CreateLikeSerializer,
    RetrieveLikeSerializer,
    UpdateLikeSerializer,
    ListLikeSerializer
)


class LikeViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    GenericViewSet
):
    """View set for like"""
    queryset = Like.objects.all()
    serializer_classes = {
            'create': CreateLikeSerializer,
            'update': UpdateLikeSerializer,
            'partial_update': UpdateLikeSerializer,
            'retrieve': RetrieveLikeSerializer,
            'list': ListLikeSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)
