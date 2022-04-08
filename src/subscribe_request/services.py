from typing import Optional

from django.db.models.query import QuerySet
from rest_framework.exceptions import AuthenticationFailed

from subscribe_request.models import SubscribeRequest
from user.models import User
from page.models import Page


def accept_all_subscribe_requests(
        queryset_subscribe_requests: QuerySet) -> None:
    for subscribe_request in queryset_subscribe_requests:
        subscribe_request.is_accept = True
        subscribe_request.initiator_page.subscriptions.add(
            subscribe_request.desired_page.owner)
        subscribe_request.desired_page.followers.add(
            subscribe_request.initiator_page.owner)
        subscribe_request.save()


def create_subscribe_request(
        current_user: User,
        initiator_page: Page,
        desired_page: Page
) -> Optional[SubscribeRequest]:
    if initiator_page.owner != current_user:
        raise AuthenticationFailed()
    if desired_page.is_private and not SubscribeRequest.objects.filter(
            initiator_page=initiator_page, desired_page=desired_page).exists():
        return SubscribeRequest.objects.create(
            initiator_page=initiator_page,
            desired_page=desired_page
        )
    else:
        desired_page.followers.add(initiator_page.owner)
        initiator_page.subscriptions.add(desired_page.owner)


def update_subscribe_request(
        initiator_page: Page,
        desired_page: Page,
        is_accept: bool
) -> None:
    if is_accept:
        desired_page.followers.add(initiator_page.owner)
        initiator_page.subscriptions.add(desired_page.owner)
