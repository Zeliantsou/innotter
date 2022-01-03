from user.models import User
from like.models import Like


def create_like(current_user: User, validated_data: dict) -> None:
    """Add like to a post if a current user did not add one and page with post is not blocked"""

    post = validated_data.get('post')
    if not Like.objects.filter(owner=current_user, post__id=post.id) and \
            not post.page.is_permanent_blocked and post.page.is_temporary_blocked():
        Like.objects.create(owner=current_user, **validated_data)
