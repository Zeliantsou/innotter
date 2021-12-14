from datetime import datetime, timedelta

from django.forms.models import model_to_dict
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)

from page.permissions import (
    IsAdminForPage,
    IsModeratorForPage,
    IsPageOwner,
    IsFollower,
    IsPublicPage,
    IsBlockedPage,
    IsBlockedOwner,
    IsBlockedUser,
)
from page.models import Page
from page.serializers import (
    CreatePageSerializer,
    UpdatePageSerializer,
    RetrievePageSerializer,
    ListPageSerializer,
    TemporaryBlockDaySerializer,
    DeleteFollowerSerializer,
    DeleteSubscriptionsSerializer,
)


class PageViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  UpdateModelMixin,
                  DestroyModelMixin,
                  ListModelMixin,
                  GenericViewSet):
    """View set for page"""
    queryset = Page.objects.all()
    # queryset = Page.objects.filter(
    #     is_permanent_blocked=False).filter(
    #     unblock_date__lt=datetime.now()).filter(
    #     owner__is_blocked=False
    # )
    # queryset = Page.objects.exclude(is_permanent_blocked=True, unblock_date__gt=datetime.now(), owner__is_blocked=True)
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
            'delete_subscriptions': (IsBlockedUser, IsPageOwner, IsBlockedPage,),
    }
    serializer_classes = {
            'create': CreatePageSerializer,
            'update': UpdatePageSerializer,
            'partial_update': UpdatePageSerializer,
            'retrieve': RetrievePageSerializer,
            'list': ListPageSerializer,
            'temporary_block': TemporaryBlockDaySerializer,
            'delete_follower': DeleteFollowerSerializer,
            'delete_subscriptions': DeleteSubscriptionsSerializer,
    }

    @action(detail=True, methods=('patch', ))
    def permanent_block(self, request, pk=None):
        page = self.get_object()
        page.is_permanent_blocked = not page.is_permanent_blocked
        page.save()
        return Response(
            status=HTTP_200_OK,
            data=model_to_dict(page, fields=('id', 'email', 'unblock_date', 'is_permanent_blocked',))
        )

    @action(detail=True, methods=('patch',))
    def temporary_block(self, request, pk=None):
        page = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        block_days = timedelta(days=serializer.validated_data.get('block_duration_days'))
        page.unblock_date = datetime.now() + block_days
        page.save()
        return Response(
            status=HTTP_200_OK,
            data=model_to_dict(page, fields=('id', 'email', 'unblock_date', 'is_permanent_blocked',))
        )

    @action(detail=True, methods=('patch',))
    def delete_follower(self, request, pk=None):
        page = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        for user in page.followers.filter(id__in=set(serializer.validated_data.get('list_ids_removable_follower'))):
            page.followers.remove(user)
        page.save()
        return Response(
            status=HTTP_200_OK,
            data=model_to_dict(page, fields=('id', 'name',))
        )

    @action(detail=True, methods=('patch',))
    def delete_subscriptions(self, request, pk=None):
        page = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        for user in page.subscriptions.filter(
                id__in=set(serializer.validated_data.get('list_user_ids_refuse_subscribe'))):
            page.subscriptions.remove(user)
        page.save()
        return Response(
            status=HTTP_200_OK,
            data=model_to_dict(page, fields=('id', 'name',))
        )

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.custom_user
        page = Page.objects.create(**serializer.validated_data)
        serializer.validated_data['id'] = page.id

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def get_permissions(self):
        permission_classes = self.permission_classes.get(self.action)
        return [permission() for permission in permission_classes]
