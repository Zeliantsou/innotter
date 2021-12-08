from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.urls import resolve

from user.services.security_service import refresh_tokens
from user.models import User
from user.serializers import (
    CreateUserSerializer,
    UpdateUserSerializer,
    RetrieveUserSerializer,
    ListUserSerializer,
    LoginSerializer,
    TokenSerializer
)
from user.services.auth_service import login


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
            'refresh_tokens': TokenSerializer
    }

    def create(self, request, *args, **kwargs):
        print('CREATE', resolve(request.path))
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=('post',))
    def refresh_tokens(self, request):
        test_url = resolve(request.path)
        print(test_url)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            status=status.HTTP_200_OK,
            data=refresh_tokens(token=serializer.validated_data.get('token'))
        )

    @action(detail=False, methods=('post',))
    def login_user(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = login(
            email=serializer.validated_data.get('email'),
            plain_password=serializer.validated_data.get('password')
        )
        return Response(
            status=status.HTTP_200_OK,
            data=tokens
        )

    def perform_create(self, serializer):
        user = User.objects.create_user(**serializer.validated_data)
        serializer.validated_data['id'] = user.id

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)
