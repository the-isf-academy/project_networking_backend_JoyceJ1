# Generated by Django 5.1.2 on 2024-10-20 08:30

import banjo.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_remove_user_user_completed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_completed',
            field=banjo.models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='posted_hunts',
            field=banjo.models.IntegerField(default=0),
        ),
    ]
