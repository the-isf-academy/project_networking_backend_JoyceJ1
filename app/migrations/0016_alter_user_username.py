# Generated by Django 5.1.2 on 2024-10-20 13:19

import banjo.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=banjo.models.StringField(default=''),
        ),
    ]
