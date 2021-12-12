from django.contrib import admin

from page.models import Page


class PageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'uuid',
        'owner',
        'image',
        'is_private',
        'unblock_date',
        'is_permanent_blocked',
    )


admin.site.register(Page, PageAdmin)
