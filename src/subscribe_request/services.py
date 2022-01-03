from django.db.models.query import QuerySet
from rest_framework.exceptions import AuthenticationFailed

from subscribe_request.models import SubscribeRequest
from user.models import User


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
        validated_data: dict
) -> None:
    initiator_page = validated_data.get('initiator_page')
    desired_page = validated_data.get('desired_page')
    if initiator_page.owner != current_user:
        raise AuthenticationFailed()
    if desired_page.is_private:
        SubscribeRequest.objects.create(**validated_data)
    else:
        desired_page.followers.add(initiator_page.owner)
        initiator_page.subscriptions.add(desired_page.owner)


def update_subscribe_request(
        current_subscribe_request: SubscribeRequest,
        is_accept: bool
) -> None:
    initiator_page = current_subscribe_request.initiator_page
    desired_page = current_subscribe_request.desired_page
    if is_accept:
        desired_page.followers.add(initiator_page.owner)
        initiator_page.subscriptions.add(desired_page.owner)
