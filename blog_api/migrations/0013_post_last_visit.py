"""
Class docstring: Brief description of the NotificationConsumer class.
"""
# Generated by Django 4.2.11 on 2024-03-13 10:17

from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Class docstring: Brief description of the NotificationConsumer class.
    """

    dependencies = [
        ('blog_api', '0012_remove_post_last_visit'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='last_visit',
            field=models.TimeField(default='03:00:45'),
        ),
    ]
