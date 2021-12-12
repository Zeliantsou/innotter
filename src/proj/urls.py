from django.contrib import admin
from django.urls import path, include
from django.conf import settings

api_prefix = settings.API_PREFIX

urlpatterns = [
    path('admin/', admin.site.urls),
    path(api_prefix, include('user.urls')),
    path(api_prefix, include('page.urls')),
    path(api_prefix, include('like.urls')),
    path(api_prefix, include('post.urls')),
    path(api_prefix, include('subscribe_request.urls')),
    path(api_prefix, include('tag.urls'))
]
