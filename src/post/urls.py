from rest_framework.routers import DefaultRouter

from post.views import PostViewSet

router = DefaultRouter()

router.register(r'posts', PostViewSet, basename='posts')
urlpatterns = router.urls
