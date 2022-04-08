from rest_framework import serializers

from user.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """Serializes user for create view"""

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UpdateUserSerializer(serializers.ModelSerializer):
    """Serializes user for update view"""

    class Meta:
        model = User
        fields = (
            'email',
            'photo_path',
            'title',
            'is_blocked',
            'role',

        )


class RetrieveUserSerializer(serializers.ModelSerializer):
    """Serializes user for retrieve view"""

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'photo_path',
            'title',
            'is_blocked',
            'role',
        )


class ListUserSerializer(serializers.ModelSerializer):
    """Serializes user for list view"""

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'photo_path',
            'title',
            'is_blocked',
            'role',
        )


class LoginSerializer(serializers.Serializer):
    """Serializes user for login"""
    email = serializers.CharField()
    password = serializers.CharField()
