from django.contrib import admin

from subscribe_request.models import SubscribeRequest


class SubscribeRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'initiator',
        'desired',
        'is_accept',
    )


admin.site.register(SubscribeRequest, SubscribeRequestAdmin)
