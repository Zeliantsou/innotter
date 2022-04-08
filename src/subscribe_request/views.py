from django.db.models import Q
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
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
from subscribe_request.services import (
    accept_all_subscribe_requests,
    create_subscribe_request,
    update_subscribe_request,
)
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
            'accept_subscribe_requests': (IsBlockedUser,),
    }
    serializer_classes = {
            'create': CreateSubscribeRequestSerializer,
            'update': UpdateSubscribeRequestSerializer,
            'partial_update': UpdateSubscribeRequestSerializer,
            'retrieve': RetrieveSubscribeRequestSerializer,
            'list': ListSubscribeRequestSerializer,
    }

    @action(detail=False, methods=('patch',))
    def accept_subscribe_requests(self, request):
        accept_all_subscribe_requests(
            queryset_subscribe_requests=self.get_queryset())
        return Response(status=HTTP_200_OK)

    def perform_create(self, serializer):
        create_subscribe_request(
            current_user=self.request.custom_user,
            initiator_page=serializer.validated_data.get('initiator_page'),
            desired_page=serializer.validated_data.get('desired_page')
        )

    def perform_update(self, serializer):
        updating_page = self.get_object()
        update_subscribe_request(
            initiator_page=updating_page.initiator_page,
            desired_page=updating_page.desired_page,
            is_accept=serializer.validated_data.get('is_accepted')
        )
        serializer.save()

    def get_queryset(self):
        user_role = self.request.custom_user.role
        if self.action == 'list' and user_role == 'user':
            return SubscribeRequest.objects.filter(
                Q(initiator_page__owner=self.request.custom_user) |
                Q(desired_page__owner=self.request.custom_user)
            )
        if self.action == 'accept_subscribe_requests' and user_role == 'user':
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
