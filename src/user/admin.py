from django.contrib import admin

from user.models import User


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'photo_path',
        'title',
        'is_blocked',
        'role'
    )
    exclude = (
        'password',
        'last_login',
        'groups',
        'first_name',
        'last_name',
        'user_permissions',
        'date_joined',
    )


admin.site.register(User, CustomUserAdmin)
