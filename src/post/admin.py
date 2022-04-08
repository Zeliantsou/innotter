from django.contrib import admin

from post.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
        'page',
        'content',
        'reply_to',
        'created',
        'updated',
    )


admin.site.register(Post, PostAdmin)
