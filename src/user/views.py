from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action

from user.services.security_service import refresh_tokens
from user.services.generic_service import (
    block_or_unblock_user,
    upload_photo_to_s3,
)
from user.models import User
from user.serializers import (
    CreateUserSerializer,
    UpdateUserSerializer,
    RetrieveUserSerializer,
    ListUserSerializer,
    LoginSerializer,
)
from user.services.auth_service import login
from user.permissions import IsAdminForUser


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """View set for user"""
    queryset = User.objects.all()
    serializer_classes = {
            'create': CreateUserSerializer,
            'update': UpdateUserSerializer,
            'partial_update': UpdateUserSerializer,
            'retrieve': RetrieveUserSerializer,
            'list': ListUserSerializer,
            'login_user': LoginSerializer,
    }

    @action(detail=False, methods=('post',))
    def refresh_tokens(self, request):
        token_data = refresh_tokens(token=request.META.get('HTTP_AUTHORIZATION', b''))
        return Response(status=status.HTTP_200_OK, data=token_data)

    @action(detail=False, methods=('post',))
    def login_user(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = login(
            email=serializer.validated_data.get('email'),
            plain_password=serializer.validated_data.get('password')
        )
        return Response(status=status.HTTP_200_OK, data=tokens)

    @action(detail=True, methods=('patch',))
    def block_user(self, request, pk=None):
        block_or_unblock_user(user=self.get_object())
        return Response(status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.validated_data['photo_path'] = upload_photo_to_s3(
            file_path=serializer.validated_data.get('photo_path')
        )
        serializer.save()

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def get_permissions(self):
        if self.action == 'block_user':
            return (IsAdminForUser(),)
        return super().get_permissions()
