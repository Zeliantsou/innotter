from django.db import models


class SubscribeRequest(models.Model):
    initiator = models.ForeignKey(
        'user.User',
        on_delete=models.SET_NULL,
        related_name='initiator_requests',
        blank=True,
        null=True
    )
    desired = models.ForeignKey(
        'user.User',
        on_delete=models.SET_NULL,
        related_name='wanted_requests',
        blank=True,
        null=True
    )
    is_accept = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f'request_{self.id}'
