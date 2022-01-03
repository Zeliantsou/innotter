from rest_framework.permissions import BasePermission


class IsHavePage(BasePermission):
    """Checks if user has one page at least"""

    def has_permission(self, request, view):
        return request.custom_user.pages.all().count() > 0


class IsTagOwner(BasePermission):
    """Checks if user is owner of tag"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.custom_user


class IsBlockedPageWithTag(BasePermission):
    """Checks if tag is attached to any page and if this page is blocked"""

    def has_object_permission(self, request, view, obj):
        for page in obj.pages.all():
            if page.is_permanent_blocked or not page.is_temporary_blocked():
                return False
        return True
