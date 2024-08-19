# Generated by Django 4.2.11 on 2024-05-07 10:56
"""
Class docstring: Brief description of the NotificationConsumer class.
"""

from django.db import migrations
import django_resized.forms

import blog_api.models


class Migration(migrations.Migration):
    """
Class docstring: Brief description of the NotificationConsumer class.
"""

    dependencies = [
        ('blog_api', '0019_alter_comment_user_alter_post_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=django_resized.forms.ResizedImageField(
                crop=None, force_format=None, keep_meta=True,
                quality=-1, scale=None, size=[(500, 300), (None, None)],
                upload_to=blog_api.models.upload_to
                ),
        ),
    ]
