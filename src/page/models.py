from pytz import UTC
from datetime import datetime

from django.db import models


class Page(models.Model):
    """Page model"""
    name = models.CharField(
        max_length=100,
    )
    uuid = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True
    )
    description = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )
    tags = models.ManyToManyField(
        'tag.Tag',
        related_name='pages'
    )
    owner = models.ForeignKey(
        'user.User',
        on_delete=models.SET_NULL,
        related_name='pages',
        blank=True,
        null=True
    )
    followers = models.ManyToManyField(
        'user.User',
        related_name='follow_pages'
    )
    subscriptions = models.ManyToManyField(
        'user.User',
        related_name='subscribe_pages'
    )
    image = models.ImageField(
        upload_to='uploads/%Y/%m/%d/',
        blank=True,
        null=True
    )
    is_private = models.BooleanField(
        default=False
    )
    unblock_date = models.DateTimeField(
        blank=True,
        null=True,
        default=datetime.now
    )
    is_permanent_blocked = models.BooleanField(
        default=False
    )

    def is_temporary_blocked(self):
        utc_now = datetime.utcnow().replace(tzinfo=UTC)
        utc_unblock_data = self.unblock_date.replace(tzinfo=UTC)
        return utc_now > utc_unblock_data

    def __str__(self):
        return self.name
