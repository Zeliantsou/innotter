# Generated by Django 4.0 on 2021-12-14 12:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='unblock_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
    ]
