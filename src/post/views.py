from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)

from post.models import Post
from post.serializers import (
    CreatePostSerializer,
    UpdatePostSerializer,
    RetrievePostSerializer,
    ListPostSerializer
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
    serializer_classes = {
            'create': CreatePostSerializer,
            'update': UpdatePostSerializer,
            'partial_update': UpdatePostSerializer,
            'retrieve': RetrievePostSerializer,
            'list': ListPostSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)
