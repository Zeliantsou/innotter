from rest_framework.filters import SearchFilter
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)

from user.permissions import IsBlockedUser
from page.permissions import (
    IsAdminForPage,
    IsModeratorForPage,
    IsPageOwner,
    IsFollower,
    IsPublicPage,
    IsBlockedPage,
    IsBlockedOwner,
)
from page.models import Page
from page.services import (
    permanent_block_or_unblock_page,
    temporary_block_page,
    add_tags_to_page,
    remove_tags_from_page,
    remove_followers_from_page,
    add_free_subscriptions_to_page,
    remove_subscriptions_from_page,
)
from page.serializers import (
    CreatePageSerializer,
    UpdatePageSerializer,
    RetrievePageSerializer,
    ListPageSerializer,
    TemporaryBlockDaySerializer,
    DeleteFollowerSerializer,
    AddFreeSubscriptionsSerializer,
    DeleteSubscriptionsSerializer,
    ActionTagSerializer,
)


class PageViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  UpdateModelMixin,
                  DestroyModelMixin,
                  ListModelMixin,
                  GenericViewSet):
    """View set for page"""
    queryset = Page.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'uuid', 'tags__name', 'owner__email')
    permission_classes = {
            'create': (IsBlockedUser,),
            'update': (IsBlockedUser, IsPageOwner, IsBlockedPage,),
            'partial_update': (IsBlockedUser, IsPageOwner, IsBlockedPage,),
            'retrieve': (IsBlockedUser, IsBlockedOwner, IsBlockedPage, IsPublicPage |
                         IsFollower | IsPageOwner | IsAdminForPage | IsModeratorForPage,),
            'list': (IsBlockedUser, ),
            'destroy': (IsBlockedUser, IsPageOwner, IsBlockedPage,),
            'permanent_block': (IsAdminForPage,),
            'temporary_block': (IsBlockedUser, IsAdminForPage | IsModeratorForPage,),
            'delete_follower': (IsBlockedUser, IsPageOwner, IsBlockedPage,),
            'add_free_subscriptions': (IsBlockedUser, IsPageOwner, IsBlockedPage,),
            'delete_subscriptions': (IsBlockedUser, IsPageOwner, IsBlockedPage,),
            'add_tag': (IsBlockedUser, IsPageOwner, IsBlockedPage,),
            'delete_tag': (IsBlockedUser, IsPageOwner, IsBlockedPage,),
    }
    serializer_classes = {
            'create': CreatePageSerializer,
            'update': UpdatePageSerializer,
            'partial_update': UpdatePageSerializer,
            'retrieve': RetrievePageSerializer,
            'list': ListPageSerializer,
            'temporary_block': TemporaryBlockDaySerializer,
            'delete_follower': DeleteFollowerSerializer,
            'add_free_subscriptions': AddFreeSubscriptionsSerializer,
            'delete_subscriptions': DeleteSubscriptionsSerializer,
            'add_tag': ActionTagSerializer,
            'delete_tag': ActionTagSerializer,
    }

    @action(detail=True, methods=('patch',))
    def permanent_block(self, request, pk=None):
        page_data = permanent_block_or_unblock_page(self.get_object())
        return Response(status=HTTP_200_OK, data=page_data)

    @action(detail=True, methods=('patch',))
    def temporary_block(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        page_data = temporary_block_page(
            self.get_object(),
            serializer.validated_data.get('block_duration_days')
        )
        return Response(status=HTTP_200_OK, data=page_data)

    @action(detail=True, methods=('patch',))
    def add_tag(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        page_data = add_tags_to_page(
            page=self.get_object(),
            set_added_tag_ids=set(serializer.validated_data.get('list_tag_ids'))
        )
        return Response(status=HTTP_200_OK, data=page_data)

    @action(detail=True, methods=('patch',))
    def delete_tag(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        page_data = remove_tags_from_page(
            page=self.get_object(),
            set_deleted_tag_ids=set(serializer.validated_data.get('list_tag_ids'))
        )
        return Response(status=HTTP_200_OK, data=page_data)

    @action(detail=True, methods=('patch',))
    def delete_follower(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        page_data = remove_followers_from_page(
            page=self.get_object(),
            set_deleted_follower_ids=set(
                serializer.validated_data.get('list_ids_removable_follower')
            )
        )
        return Response(status=HTTP_200_OK, data=page_data)

    @action(detail=True, methods=('patch', ))
    def add_free_subscriptions(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        page_data = add_free_subscriptions_to_page(
            page=self.get_object(),
            set_user_ids_add_to_subscriptions=set(
                serializer.validated_data.get('list_user_ids_add_subscribe')
            )
        )
        return Response(status=HTTP_200_OK, data=page_data)

    @action(detail=True, methods=('patch',))
    def delete_subscriptions(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        page_data = remove_subscriptions_from_page(
            page=self.get_object(),
            set_user_ids_remove_from_subscriptions=set(
                serializer.validated_data.get('list_user_ids_refuse_subscribe')
            )
        )
        return Response(status=HTTP_200_OK, data=page_data)

    def perform_create(self, serializer):
        Page.objects.create(owner=self.request.custom_user, **serializer.validated_data)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def get_permissions(self):
        permission_classes = self.permission_classes.get(self.action)
        return [permission() for permission in permission_classes]
