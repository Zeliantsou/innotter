from user.models import User
from like.models import Like
from post.models import Post


def create_like(current_user: User, liked_post: Post) -> None:
    """Add like to a post if a current user did not add one and page with post is not blocked"""

    if not Like.objects.filter(owner=current_user, post__id=liked_post.id).exists() and \
            not liked_post.page.is_permanent_blocked and \
            liked_post.page.is_temporary_blocked():
        Like.objects.create(owner=current_user, post=liked_post)
