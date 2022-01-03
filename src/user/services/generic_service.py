from boto3 import client

from django.conf import settings
from rest_framework.exceptions import ValidationError

from user.models import User


def block_or_unblock_user(user: User) -> None:
    user.is_blocked = not user.is_blocked
    user.save()
    for page in user.pages.all():
        if user.is_blocked:
            page.is_permanent_blocked = True
        else:
            page.is_permanent_blocked = False
        page.save()


def is_allowed_file_extension(file_path: str) -> bool:
    return file_path.split('.')[-1] in settings.ALLOWED_FILE_EXTENSIONS


def get_file_name(file_path: str) -> str:
    name = file_path.split('.')[-2]
    extension = file_path.split('.')[-1]
    return name + '.' + extension


def upload_photo_to_s3(file_path: str) -> str:
    if not is_allowed_file_extension(file_path=file_path):
        raise ValidationError()
    s3_client = client('s3')
    key = get_file_name(file_path=file_path)
    s3_client.put_object(
        Body=file_path,
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=key
    )
    presigned_url = s3_client.generate_presigned_url(
        'put_object',
        Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': key},
        ExpiresIn=3600
    )
    return presigned_url
