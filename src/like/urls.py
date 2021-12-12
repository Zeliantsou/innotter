from rest_framework.routers import DefaultRouter

from like.views import LikeViewSet

router = DefaultRouter()

router.register(r'likes', LikeViewSet, basename='likes')
urlpatterns = router.urls
