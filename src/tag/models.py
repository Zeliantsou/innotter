from django.db import models


class Tag(models.Model):
    owner = models.ForeignKey(
        'user.User',
        on_delete=models.SET_NULL,
        related_name='tags',
        blank=True,
        null=True
    )
    name = models.CharField(
        max_length=30
    )

    def __str__(self):
        return self.name
