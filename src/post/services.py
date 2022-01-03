from user.models import User
from post.models import Post

from post.tasks import notify_followers_about_new_post


def create_post(current_user: User, validated_data: dict) -> None:
    reply_to = validated_data.get('reply_to')
    page = validated_data.get('page')
    created_post = None
    if reply_to and not reply_to.page.is_permanent_blocked and reply_to.page.is_temporary_blocked():
        validated_data['page'] = reply_to.page
        created_post = Post.objects.create(owner=current_user, **validated_data)
    if not reply_to and page and not page.is_permanent_blocked and page.check_temporary_block():
        created_post = Post.objects.create(owner=current_user, **validated_data)
    if created_post:
        follower_list = [follower.email for follower in created_post.page.followers.all()]
        notify_followers_about_new_post.delay(created_post.owner.email, follower_list)
