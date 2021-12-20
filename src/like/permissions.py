from datetime import datetime
import pytz

from rest_framework.permissions import BasePermission

utc = pytz.UTC


class IsLikeOwner(BasePermission):
    """Checks if user is an owner of like"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.custom_user


class IsAdminForLike(BasePermission):
    """Checks if user is an admin"""

    def has_object_permission(self, request, view, obj):
        return request.custom_user.role == 'admin'


class IsModeratorForLike(BasePermission):
    """Checks if user is a moderator"""

    def has_object_permission(self, request, view, obj):
        return request.custom_user.role == 'moderator'


class IsBlockedPage(BasePermission):
    """Checks if page with post that has current like is blocked"""

    def has_object_permission(self, request, view, obj):
        utc_unblock_datetime = obj.post.page.unblock_date.replace(tzinfo=utc)
        utc_datetime_now = datetime.utcnow().replace(tzinfo=utc)
        return not obj.post.page.is_permanent_blocked and utc_unblock_datetime < utc_datetime_now

