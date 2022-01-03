from rest_framework.permissions import BasePermission


class IsAdminForPage(BasePermission):
    """Checks if user has 'admin' role"""

    def has_object_permission(self, request, view, obj):
        return request.custom_user.role == 'admin'


class IsModeratorForPage(BasePermission):
    """Checks if user has 'moderator' role"""

    def has_object_permission(self, request, view, obj):
        return request.custom_user.role == 'moderator'


class IsPageOwner(BasePermission):
    """Checks if the user is an owner of certain page"""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.custom_user:
            return True
        return False


class IsFollower(BasePermission):
    """Checks if the user is a follower of certain page"""

    def has_object_permission(self, request, view, obj):
        if obj.is_private and request.custom_user in obj.followers.all():
            return True
        return False


class IsPublicPage(BasePermission):
    """Checks if the page is public"""

    def has_object_permission(self, request, view, obj):
        return not obj.is_private


class IsBlockedPage(BasePermission):
    """Check if the page is blocked"""

    def has_object_permission(self, request, view, obj):
        return not obj.is_permanent_blocked and obj.is_temporary_blocked()


class IsBlockedOwner(BasePermission):
    """Check if the owner of page is blocked"""

    def has_object_permission(self, request, view, obj):
        return not obj.owner.is_blocked
