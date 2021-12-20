from datetime import datetime

from django.db.models import Q
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)

from user.permissions import IsBlockedUser
from post.models import Post
from post.serializers import (
    CreatePostSerializer,
    UpdatePostSerializer,
    RetrievePostSerializer,
    ListPostSerializer
)
from post.permissions import (
    IsPageOwnerBlocked,
    IsPageBlocked,
    IsPostOwner,
    IsPagePrivate,
    IsPageOwner,
    IsAdminForPost,
    IsModeratorForPost,
    IsPageFollower,
)


class PostViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    GenericViewSet
):
    queryset = Post.objects.all()
    permission_classes = {
            'create': (IsBlockedUser,),
            'update': (IsBlockedUser, IsPageOwnerBlocked, IsPageBlocked, IsPostOwner,),
            'partial_update': (IsBlockedUser, IsPageOwnerBlocked, IsPageBlocked, IsPostOwner,),
            'retrieve': (IsBlockedUser, IsPageOwnerBlocked, IsPageBlocked, IsPagePrivate |
                         IsPageOwner | IsPostOwner | IsAdminForPost | IsModeratorForPost | IsPageFollower,),
            'list': (IsBlockedUser,),
            'destroy': (IsBlockedUser, IsPageOwner | IsPostOwner | IsAdminForPost | IsModeratorForPost,),
    }
    serializer_classes = {
            'create': CreatePostSerializer,
            'update': UpdatePostSerializer,
            'partial_update': UpdatePostSerializer,
            'retrieve': RetrievePostSerializer,
            'list': ListPostSerializer,
    }

    def perform_create(self, serializer):
        reply_to = serializer.validated_data.get('reply_to')
        page = serializer.validated_data.get('page')
        if reply_to and not reply_to.page.is_permanent_blocked and reply_to.page.check_temporary_block():
            serializer.validated_data['page'] = reply_to.page
            Post.objects.create(owner=self.request.custom_user, **serializer.validated_data)
        if not reply_to and page and not page.is_permanent_blocked and page.check_temporary_block():
            Post.objects.create(owner=self.request.custom_user, **serializer.validated_data)

    def get_queryset(self):
        if self.action == 'list' and self.request.custom_user.role == 'user':
            return Post.objects.filter(
                Q(page__is_permanent_blocked=False) &
                Q(page__unblock_date__lt=datetime.now()) &
                Q(page__owner__is_blocked=False)).filter(
                Q(page__is_private=False) |
                Q(owner=self.request.custom_user) |
                Q(page__owner=self.request.custom_user) |
                Q(page__followers__in=(self.request.custom_user,))
            )
        return self.queryset

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def get_permissions(self):
        permissions_classes = self.permission_classes.get(self.action)
        return [permission() for permission in permissions_classes]
