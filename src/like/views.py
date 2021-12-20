from datetime import datetime
import pytz

from rest_framework.viewsets import GenericViewSet
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
    ListLikeSerializer
)
from user.permissions import IsBlockedUser
from like.permissions import (
    IsLikeOwner,
    IsBlockedPage,
    IsAdminForLike,
    IsModeratorForLike,
)

utc = pytz.UTC


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
        post = serializer.validated_data.get('post')
        if not Like.objects.filter(owner=self.request.custom_user, post__id=post.id) and\
                not post.page.is_permanent_blocked and \
                post.page.unblock_date.replace(tzinfo=utc) < datetime.now().replace(tzinfo=utc):
            serializer.validated_data['owner'] = self.request.custom_user
            Like.objects.create(**serializer.validated_data)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def get_permissions(self):
        permission_classes = self.permission_classes.get(self.action)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.action == 'list' and self.request.custom_user.role == 'user':
            return Like.objects.filter(owner=self.request.custom_user)
        return self.queryset
