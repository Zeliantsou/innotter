from rest_framework.permissions import BasePermission


class IsBlockedUser(BasePermission):
    """Check if the user is blocked"""

    def has_permission(self, request, view):
        print('1-block user', not request.custom_user.is_blocked)
        return not request.custom_user.is_blocked
