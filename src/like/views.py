from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)

from user.permissions import IsBlockedUser
from like.services import create_like
from like.models import Like
from like.serializers import (
    CreateLikeSerializer,
    RetrieveLikeSerializer,
    ListLikeSerializer
)
from like.permissions import (
    IsLikeOwner,
    IsBlockedPage,
    IsAdminForLike,
    IsModeratorForLike,
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
    permission_classes = {
            'create': (IsBlockedUser,),
            'retrieve': (IsBlockedUser, IsLikeOwner | IsAdminForLike | IsModeratorForLike,),
            'list': (IsBlockedUser,),
            'destroy': (IsBlockedUser, IsLikeOwner, IsBlockedPage,),
    }
    serializer_classes = {
            'create': CreateLikeSerializer,
            'retrieve': RetrieveLikeSerializer,
            'list': ListLikeSerializer,
    }

    def perform_create(self, serializer):
        create_like(
            current_user=self.request.custom_user,
            liked_post=serializer.validated_data.get('post')
        )

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def get_permissions(self):
        permission_classes = self.permission_classes.get(self.action)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.action == 'list' and self.request.custom_user.role == 'user':
            return Like.objects.filter(owner=self.request.custom_user)
        return self.queryset
