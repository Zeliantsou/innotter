from datetime import datetime
import pytz

from rest_framework.permissions import BasePermission

utc = pytz.UTC


class IsAdminForPage(BasePermission):
    """Checks if user has 'admin' role"""

    def has_object_permission(self, request, view, obj):
        print('7-admin', request.custom_user.role == 'admin')
        return request.custom_user.role == 'admin'


class IsModeratorForPage(BasePermission):
    """Checks if user has 'moderator' role"""

    def has_object_permission(self, request, view, obj):
        print('8-moderator', request.custom_user.role == 'moderator')
        return request.custom_user.role == 'moderator'


class IsPageOwner(BasePermission):
    """Checks if the user is an owner of certain page"""

    def has_object_permission(self, request, view, obj):
        print('6-page owner', obj.owner == request.custom_user)
        if obj.owner == request.custom_user:
            return True
        return False


class IsFollower(BasePermission):
    """Checks if the user is a follower of certain page"""

    def has_object_permission(self, request, view, obj):
        print('5-follower', obj.is_private and request.custom_user in obj.followers.all())
        if obj.is_private and request.custom_user in obj.followers.all():
            return True
        return False


class IsPublicPage(BasePermission):
    """Checks if the page is public"""

    def has_object_permission(self, request, view, obj):
        print('4-public page', not obj.is_private)
        return not obj.is_private


class IsBlockedPage(BasePermission):
    """Check if the page is blocked"""

    def has_object_permission(self, request, view, obj):
        utc_unblock_datetime = obj.unblock_date.replace(tzinfo=utc)
        utc_datetime_now = datetime.utcnow().replace(tzinfo=utc)
        print('3-block page', not obj.is_permanent_blocked and utc_unblock_datetime < utc_datetime_now)
        return not obj.is_permanent_blocked and utc_unblock_datetime < utc_datetime_now


class IsBlockedOwner(BasePermission):
    """Check if the owner of page is blocked"""

    def has_object_permission(self, request, view, obj):
        print('2-block page owner', not obj.owner.is_blocked)
        return not obj.owner.is_blocked
