from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)

from user.permissions import IsBlockedUser
from tag.models import Tag
from tag.serializers import (
    CreateTagSerializer,
    RetrieveTagSerializer,
    UpdateTagSerializer,
    ListTagSerializer
)
from tag.permissions import (
    IsHavePage,
    IsTagOwner,
    IsBlockedPageWithTag,
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
    permission_classes = {
            'create': (IsBlockedUser, IsHavePage,),
            'update': (IsBlockedUser, IsTagOwner, IsBlockedPageWithTag,),
            'partial_update': (IsBlockedUser, IsTagOwner, IsBlockedPageWithTag,),
            'retrieve': (IsBlockedUser,),
            'list': (IsBlockedUser, IsTagOwner),
            'destroy': (IsBlockedUser, IsTagOwner, IsBlockedPageWithTag,),
    }
    serializer_classes = {
            'create': CreateTagSerializer,
            'update': UpdateTagSerializer,
            'partial_update': UpdateTagSerializer,
            'retrieve': RetrieveTagSerializer,
            'list': ListTagSerializer,
    }

    def perform_create(self, serializer):
        Tag.objects.create(owner=self.request.custom_user, **serializer.validated_data)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def get_permissions(self):
        permission_classes = self.permission_classes.get(self.action)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.action == 'list' and self.request.custom_user.role == 'user':
            return Tag.objects.filter(owner=self.request.custom_user)
        return self.queryset
