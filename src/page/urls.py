from rest_framework.routers import DefaultRouter

from page.views import PageViewSet

router = DefaultRouter()

router.register(r'pages', PageViewSet, basename='pages')
urlpatterns = router.urls
