# Generated by Django 5.1.2 on 2024-10-21 12:19

import banjo.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_remove_scavenger_hunt_posted_user_user_posted_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='posted_user',
        ),
        migrations.AddField(
            model_name='scavenger_hunt',
            name='posted_user',
            field=banjo.models.StringField(default=''),
        ),
    ]