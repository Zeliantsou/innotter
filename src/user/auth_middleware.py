from rest_framework import exceptions

from django.conf import settings
from django.urls import resolve

from user.models import User
from user.services.security_service import decode_token
from user.views import UserViewSet


class CustomAuthMiddleware:
    """Custom class for middleware. Adds user to request"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_urls = settings.ALLOWED_URLS
        url_name = resolve(request.path).url_name
        if url_name in allowed_urls and request.method == allowed_urls[url_name]:
            return self.get_response(request)
        print(request.META)
        print(request.META.get('HTTP_AUTHORIZATION', b''))
        token_data = decode_token(request.META.get('HTTP_AUTHORIZATION', b''))
        print(token_data)
        try:
            user = User.objects.get(id=token_data.get('subject'))
        except User.DoesNotExist:
            raise exceptions.PermissionDenied()
        # if request.path in settings.ONLY_ADMIN_URLS and user.role != 'admin':
        #     raise exceptions.PermissionDenied()
        request.user = user
        response = self.get_response(request)
        return response

