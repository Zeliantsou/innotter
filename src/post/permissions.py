from rest_framework.permissions import BasePermission


class IsPageOwnerBlocked(BasePermission):
    """Checks if an owner of page is blocked"""

    def has_object_permission(self, request, view, obj):
        return not obj.page.owner.is_blocked


class IsPageBlocked(BasePermission):
    """Checks if page is blocked"""

    def has_object_permission(self, request, view, obj):
        return not obj.page.is_permanent_blocked and \
               obj.page.check_temporary_block()


class IsPostOwner(BasePermission):
    """Checks if user is an owner of post"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.custom_user


class IsPagePrivate(BasePermission):
    """Checks if page with post is private"""

    def has_object_permission(self, request, view, obj):
        return not obj.page.is_private


class IsPageOwner(BasePermission):
    """Checks if user with post is an owner of page"""

    def has_object_permission(self, request, view, obj):
        return obj.page.owner == request.custom_user


class IsAdminForPost(BasePermission):
    """Checks if user is an admin"""

    def has_object_permission(self, request, view, obj):
        return request.custom_user.role == 'admin'


class IsModeratorForPost(BasePermission):
    """Checks if user is a moderator"""

    def has_object_permission(self, request, view, obj):
        return request.custom_user.role == 'moderator'


class IsPageFollower(BasePermission):
    """Checks if user is a follower of page with post"""

    def has_object_permission(self, request, view, obj):
        return request.custom_user in obj.page.followers.all()
