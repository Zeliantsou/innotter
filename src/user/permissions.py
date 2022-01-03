from rest_framework.permissions import BasePermission


class IsBlockedUser(BasePermission):
    """Check if the user is blocked"""

    def has_permission(self, request, view):
        return not request.custom_user.is_blocked


class IsAdminForUser(BasePermission):
    """Check if user is admin"""

    def has_object_permission(self, request, view, obj):
        return request.custom_user.role == 'admin'
