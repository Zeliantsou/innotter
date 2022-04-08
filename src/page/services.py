from datetime import datetime, timedelta

from django.db.models import Q, Count

from user.models import User
from page.models import Page
from tag.models import Tag


def permanent_block_or_unblock_page(page: Page) -> Page:
    page.is_permanent_blocked = not page.is_permanent_blocked
    page.save()
    return page


def temporary_block_page(page: Page, block_days: int) -> Page:
    page.unblock_date = datetime.now() + timedelta(days=block_days)
    page.save()
    return page


def add_tags_to_page(page: Page, set_added_tag_ids: set) -> Page:
    for tag in Tag.objects.filter(
            Q(id__in=set_added_tag_ids) & Q(owner=page.owner)):
        page.tags.add(tag)
    page.save()
    return page


def remove_tags_from_page(page: Page, set_deleted_tag_ids: set) -> Page:
    for tag in Tag.objects.filter(
            Q(id__in=set_deleted_tag_ids) & Q(owner=page.owner)):
        page.tags.remove(tag)
    page.save()
    return page


def remove_followers_from_page(page: Page, set_deleted_follower_ids: set) -> Page:
    for follower in page.followers.filter(id__in=set_deleted_follower_ids):
        page.followers.remove(follower)
        for follower_page in follower.pages.filter(subscriptions=page.owner):
            follower_page.subscriptions.remove(page.owner)
    page.save()
    return page


def add_free_subscriptions_to_page(
        page: Page, set_user_ids_add_to_subscriptions: set) -> Page:
    for added_user_to_subscriptions in User.objects.annotate(
            num_pages=Count('pages')).filter(
            Q(id__in=set_user_ids_add_to_subscriptions) &
            Q(num_pages__gt=0)
    ):
        page.subscriptions.add(added_user_to_subscriptions)
        for page_of_added_user in added_user_to_subscriptions.pages.filter(is_private=False):
            page_of_added_user.followers.add(page.owner)
            page_of_added_user.save()
    page.save()
    return page


def remove_subscriptions_from_page(page: Page, set_user_ids_remove_from_subscriptions: set) -> Page:
    for user in page.subscriptions.filter(d__in=set_user_ids_remove_from_subscriptions):
        page.subscriptions.remove(user)
        for subscription_page in user.pages.filter(followers=page.owner):
            subscription_page.followers.remove(page.owner)
            subscription_page.save()
    page.save()
    return page
