from django.contrib import admin

from like.models import Like


class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'post',
        'owner',
    )


admin.site.register(Like, LikeAdmin)
