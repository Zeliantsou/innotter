from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)

from page.models import Page
from page.serializers import (
    CreatePageSerializer,
    UpdatePageSerializer,
    RetrievePageSerializer,
    ListPageSerializer
)


class PageViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  UpdateModelMixin,
                  DestroyModelMixin,
                  ListModelMixin,
                  GenericViewSet):
    """View set for page"""
    queryset = Page.objects.all()
    serializer_classes = {
            'create': CreatePageSerializer,
            'update': UpdatePageSerializer,
            'partial_update': UpdatePageSerializer,
            'retrieve': RetrievePageSerializer,
            'list': ListPageSerializer,
    }

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.custom_user
        page = Page.objects.create(**serializer.validated_data)
        serializer.validated_data['id'] = page.id

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)
