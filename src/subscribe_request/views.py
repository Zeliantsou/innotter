from django.db.models import Q
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)

from user.permissions import IsBlockedUser
from subscribe_request.models import SubscribeRequest
from subscribe_request.serializers import (
    CreateSubscribeRequestSerializer,
    RetrieveSubscribeRequestSerializer,
    UpdateSubscribeRequestSerializer,
    ListSubscribeRequestSerializer,
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
    permission_classes = {
            'create': (IsBlockedUser,),
            'update': (IsBlockedUser,),
            'partial_update': (IsBlockedUser,),
            'retrieve': (IsBlockedUser,),
            'list': (IsBlockedUser,),
            'destroy': (IsBlockedUser,),
            'accept_all_subscribe_requests': (IsBlockedUser,),
    }
    serializer_classes = {
            'create': CreateSubscribeRequestSerializer,
            'update': UpdateSubscribeRequestSerializer,
            'partial_update': UpdateSubscribeRequestSerializer,
            'retrieve': RetrieveSubscribeRequestSerializer,
            'list': ListSubscribeRequestSerializer,
    }

    @action(detail=False, methods=('patch',))
    def accept_all_subscribe_requests(self, request):
        for subscribe_request in self.get_queryset():
            subscribe_request.is_accept = True
            subscribe_request.initiator_page.subscriptions.add(subscribe_request.desired_page.owner)
            subscribe_request.desired_page.followers.add(subscribe_request.initiator_page.owner)
            subscribe_request.save()
        return Response(status=HTTP_200_OK)

    def perform_create(self, serializer):
        initiator_page = serializer.validated_data.get('initiator_page')
        desired_page = serializer.validated_data.get('desired_page')
        if initiator_page.owner != self.request.custom_user:
            raise AuthenticationFailed()
        if desired_page.is_private:
            SubscribeRequest.objects.create(**serializer.validated_data)
        else:
            desired_page.followers.add(initiator_page.owner)
            initiator_page.subscriptions.add(desired_page.owner)

    def perform_update(self, serializer):
        current_subscribe_request = self.get_object()
        initiator_page = current_subscribe_request.initiator_page
        desired_page = current_subscribe_request.desired_page
        if serializer.validated_data.get('is_accept'):
            desired_page.followers.add(initiator_page.owner)
            initiator_page.subscriptions.add(desired_page.owner)
        serializer.save()

    def get_queryset(self):
        user_role = self.request.custom_user.role
        if self.action == 'list' and user_role == 'user':
            return SubscribeRequest.objects.filter(
                Q(initiator_page__owner=self.request.custom_user) |
                Q(desired_page__owner=self.request.custom_user)
            )
        if self.action == 'accept_all_subscribe_requests' and user_role == 'user':
            return SubscribeRequest.objects.filter(
                Q(desired_page__owner=self.request.custom_user) &
                Q(is_accept=False)
            )
        return self.queryset

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def get_permissions(self):
        permission_classes = self.permission_classes.get(self.action)
        return [permission() for permission in permission_classes]
