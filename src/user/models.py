from django.db import models
from django.contrib.auth.models import AbstractUser

from user.manager import CustomUserManager


class User(AbstractUser):
    """Custom user model"""
    class Role(models.TextChoices):
        ADMIN = 'admin'
        MODERATOR = 'moderator'
        USER = 'user'
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    email = models.EmailField(
        'email',
        unique=True
    )
    photo_path = models.CharField(
        'photo',
        max_length=100,
        blank=True,
        null=True,
    )
    title = models.CharField(
        'title',
        max_length=100,
        blank=True,
        null=True,
    )
    is_blocked = models.BooleanField(
        'is blocked',
        default=False
    )
    role = models.CharField(
        'role',
        max_length=9,
        choices=Role.choices,
        default='user'
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
