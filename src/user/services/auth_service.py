from typing import Optional

from rest_framework import exceptions

from user.models import User
from user.services.security_service import generate_tokens


def authenticate(email: str, plain_password: str) -> Optional[User]:
    """Authenticate user"""
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise exceptions.NotFound()
    if user.check_password(plain_password):
        return user
    return None


def login(email: str, plain_password: str) -> Optional[dict]:
    """Login user"""
    user = authenticate(
        email=email,
        plain_password=plain_password
    )
    if user:
        return generate_tokens(user.id)
    raise exceptions.NotFound()
