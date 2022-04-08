import boto3
from django.conf import settings

from celery_tasks.celery import app


@app.task
def notify_followers_about_new_post(post_owner, follower_list):
    ses = boto3.client('ses')
    ses.send_email(
        Source=settings.SOURCE_EMAIL,
        Destination={'ToAddresses': follower_list},
        Message={
            'Subject': {
                'Data': f'New post from {post_owner}!!!',
                'Charset': 'utf-8'
            },
            'Body': {
                'Text': {
                    'Data': f'{post_owner} has published a new post',
                    'Charset': 'utf-8'
                },
            }
        }
    )
