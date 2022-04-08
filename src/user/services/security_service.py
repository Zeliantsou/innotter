from typing import Any, Union
from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext
from rest_framework import exceptions
from django.conf import settings

from user.models import User


pwd_context = CryptContext(schemes=("bcrypt",), deprecated="auto")


def create_token(subject: Any, timedelta_days: int) -> bytes:
    """Base method for creating tokens"""
    expire = datetime.now() + timedelta(days=int(timedelta_days))
    expire = expire.strftime(settings.FORMAT_STRING_FROM_TIME)
    payload = {
        'subject': str(subject),
        'expire': expire
    }
    return jwt.encode(
        payload=payload,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def decode_token(token: bytes) -> dict:
    """Decode token"""
    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.SECRET_KEY,
            algorithms=(settings.ALGORITHM,)
        )
    except jwt.exceptions.InvalidTokenError:
        raise exceptions.NotAuthenticated()
    return payload


def check_expiration_date(exp_date: Union[str, datetime]) -> bool:
    if isinstance(exp_date, str):
        exp_date = datetime.strptime(
            exp_date, settings.FORMAT_STRING_FROM_TIME)
    return exp_date > datetime.now()


def create_access_token(user_id: int) -> bytes:
    """Create access token"""
    return create_token(
        subject=user_id,
        timedelta_days=settings.ACCESS_TOKEN_EXPIRE_DAYS
    )


def create_refresh_token(user_id: int) -> bytes:
    """Create refresh token"""
    return create_token(
        subject=user_id,
        timedelta_days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )


def generate_tokens(user_id: int) -> dict:
    """Generate dict with access and refresh tokens"""
    return {
        'access_token': create_access_token(user_id),
        'refresh_token': create_refresh_token(user_id)
    }


def refresh_tokens(token: bytes) -> dict:
    token_data = decode_token(token=token)
    try:
        user = User.objects.get(id=token_data.get('subject'))
    except User.DoesNotExist:
        raise exceptions.NotAuthenticated()
    if not check_expiration_date(token_data.get('expire')):
        raise exceptions.NotAuthenticated()
    return generate_tokens(user_id=user.id)


def get_password_hash(plain_password: str) -> str:
    """Get hash from plain password"""
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password:str) -> bool:
    """Match plain password and hashed password"""
    return pwd_context.verify(plain_password, hashed_password)
