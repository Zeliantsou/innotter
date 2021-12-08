from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import make_password


class CustomUserManager(UserManager):
    """Custom manager for user"""

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        if not password:
            raise ValueError('User should provide a password')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self._create_user(email, password, **extra_fields)
