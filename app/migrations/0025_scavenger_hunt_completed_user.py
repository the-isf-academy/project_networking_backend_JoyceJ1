# Generated by Django 5.1.2 on 2024-10-21 12:39

import banjo.models
import django.db.models.deletion
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_rename_posted_user_scavenger_hunt_user_posted_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scavenger_hunt',
            name='completed_user',
            field=banjo.models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='completed_hunts', to='app.user'),
        ),
    ]
