from datetime import datetime
import pytz

utc = pytz.UTC

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
        blocked_pages_with_tag = 0
        for page in obj.pages.all():
            utc_unblock_datetime = page.unblock_date.replace(tzinfo=utc)
            utc_datetime_now = datetime.now().replace(tzinfo=utc)
            if page.is_permanent_blocked or utc_unblock_datetime > utc_datetime_now:
                blocked_pages_with_tag += 1
        return blocked_pages_with_tag == 0



