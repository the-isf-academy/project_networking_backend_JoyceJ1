# Generated by Django 5.1.2 on 2024-10-15 06:45

import banjo.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_scavenger_hunt_hint_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scavenger_hunt',
            name='current',
            field=banjo.models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='scavenger_hunt',
            name='day',
            field=banjo.models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='scavenger_hunt',
            name='hint',
            field=banjo.models.StringField(default=''),
        ),
        migrations.AddField(
            model_name='scavenger_hunt',
            name='month',
            field=banjo.models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='scavenger_hunt',
            name='time_limit',
            field=banjo.models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='scavenger_hunt',
            name='year',
            field=banjo.models.IntegerField(default=0),
        ),
    ]