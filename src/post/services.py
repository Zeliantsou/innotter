from typing import Optional

from user.models import User
from post.models import Post
from page.models import Page

from post.tasks import notify_followers_about_new_post


def create_post(current_user: User, page: Page,
                content: str, reply_to: Post) -> Optional[Post]:
    created_post = None
    if reply_to and not reply_to.page.is_permanent_blocked and reply_to.page.is_temporary_blocked():
        created_post = Post.objects.create(owner=current_user, page=reply_to.page,
                                           content=content, reply_to=reply_to)
    if not reply_to and page and not page.is_permanent_blocked and page.is_temporary_blocked():
        created_post = Post.objects.create(owner=current_user,
                                           page=page,
                                           content=content)
    if created_post:
        follower_list = [follower.email for follower in created_post.page.followers.all()]
        notify_followers_about_new_post.delay(created_post.owner.email, follower_list)
        return created_post
