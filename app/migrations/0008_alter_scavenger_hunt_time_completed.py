# Generated by Django 5.1.2 on 2024-10-19 19:50

import banjo.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_scavenger_hunt_time_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scavenger_hunt',
            name='time_completed',
            field=banjo.models.StringField(default=''),
        ),
    ]
