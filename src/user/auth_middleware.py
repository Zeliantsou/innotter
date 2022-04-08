from rest_framework import exceptions

from django.conf import settings
from django.urls import resolve

from user.models import User
from user.services.security_service import decode_token


class CustomAuthMiddleware:
    """Custom class for middleware. Adds user to request"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_urls = settings.ALLOWED_URLS
        resolved_path = resolve(request.path)
        url_name = resolved_path.url_name
        app_name = resolved_path.app_name
        if (url_name in allowed_urls and request.method == allowed_urls[url_name]) or app_name == 'admin':
            return self.get_response(request)
        token_data = decode_token(request.META.get('HTTP_AUTHORIZATION', b''))
        try:
            user = User.objects.get(id=token_data.get('subject'))
        except User.DoesNotExist:
            raise exceptions.PermissionDenied()
        request.custom_user = user
        response = self.get_response(request)
        return response
