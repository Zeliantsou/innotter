from datetime import datetime, timedelta

from django.db.models import Q, Count

from user.models import User
from page.models import Page
from tag.models import Tag


def permanent_block_or_unblock_page(page: Page) -> dict:
    page.is_permanent_blocked = not page.is_permanent_blocked
    page.save()
    return {
        'id': page.id,
        'is_permanent_blocked': page.is_permanent_blocked,
    }


def temporary_block_page(page: Page, block_days: int) -> dict:
    page.unblock_date = datetime.now() + timedelta(days=block_days)
    page.save()
    return {
        'id': page.id,
        'unblock_date': page.unblock_date,
    }


def add_tags_to_page(page: Page, set_added_tag_ids: set) -> dict:
    for tag in Tag.objects.filter(Q(id__in=set_added_tag_ids) & Q(owner=page.owner)):
        page.tags.add(tag)
    page.save()
    return {
        'id': page.id,
        'tags': [v['id'] for v in page.tags.all().values('id')]
    }


def remove_tags_from_page(page: Page, set_deleted_tag_ids: set) -> dict:
    for tag in Tag.objects.filter(Q(id__in=set_deleted_tag_ids) & Q(owner=page.owner)):
        page.tags.remove(tag)
    page.save()
    return {
        'id': page.id,
        'tags': [v['id'] for v in page.tags.all().values('id')]
    }


def remove_followers_from_page(page: Page, set_deleted_follower_ids: set) -> dict:
    for follower in page.followers.filter(id__in=set_deleted_follower_ids):
        page.followers.remove(follower)
        for follower_page in follower.pages.filter(subscriptions=page.owner):
            follower_page.subscriptions.remove(page.owner)
    page.save()
    return {
        'id': page.id,
        'followers': [v['id'] for v in page.followers.all().values('id')]
    }


def add_free_subscriptions_to_page(page: Page, set_user_ids_add_to_subscriptions: set) -> dict:
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
    return {
        'id': page.id,
        'subscriptions': [v['id'] for v in page.subscriptions.all().values('id')]
    }


def remove_subscriptions_from_page(page: Page, set_user_ids_remove_from_subscriptions: set) -> dict:
    for user in page.subscriptions.filter(d__in=set_user_ids_remove_from_subscriptions):
        page.subscriptions.remove(user)
        for subscription_page in user.pages.filter(followers=page.owner):
            subscription_page.followers.remove(page.owner)
            subscription_page.save()
    page.save()
    return {
        'id': page.id,
        'subscriptions': [v['id'] for v in page.subscriptions.all().values('id')]
    }
