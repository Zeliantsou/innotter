# Generated by Django 4.0 on 2021-12-12 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_managers'),
        ('page', '0002_initial'),
        ('subscribe_request', '0003_rename_desired_page_subscriberequest_desired'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriberequest',
            name='desired',
        ),
        migrations.AddField(
            model_name='subscriberequest',
            name='desired_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subscribe_requests', to='page.page'),
        ),
        migrations.AlterField(
            model_name='subscriberequest',
            name='initiator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subscribe_requests', to='user.user'),
        ),
    ]