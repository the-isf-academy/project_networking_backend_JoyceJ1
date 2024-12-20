# Generated by Django 5.1.2 on 2024-10-21 12:33

import banjo.models
import django.db.models.deletion
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_alter_scavenger_hunt_posted_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scavenger_hunt',
            old_name='posted_user',
            new_name='user_posted',
        ),
        migrations.RemoveField(
            model_name='scavenger_hunt',
            name='completed_user',
        ),
        migrations.AlterField(
            model_name='scavenger_hunt',
            name='my_user',
            field=banjo.models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='engaged_hunts', to='app.user'),
        ),
    ]
