from django.db import models


class Post(models.Model):
    owner = models.ForeignKey(
        'user.User',
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True
    )
    page = models.ForeignKey(
        'page.Page',
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True
    )
    content = models.CharField(
        max_length=300,
    )
    reply_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='children',
        blank=True,
        null=True
    )
    created = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True,
        null=True
    )
    updated = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'post_{self.id}'
