# Generated by Django 4.0 on 2021-12-12 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_request', '0002_alter_subscriberequest_desired_page_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscriberequest',
            old_name='desired_page',
            new_name='desired',
        ),
    ]
