from rest_framework.routers import DefaultRouter

from subscribe_request.views import SubscribeRequestViewSet

router = DefaultRouter()

router.register(r'subscribe_requests', SubscribeRequestViewSet, basename='subscribe_requests')
urlpatterns = router.urls
