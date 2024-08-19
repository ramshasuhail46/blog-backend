# Generated by Django 4.2.11 on 2024-04-17 12:50
"""
Class docstring: Brief description of the NotificationConsumer class.
"""
from django.db import migrations, models
import blog_api.models


class Migration(migrations.Migration):
    """
    Class docstring: Brief description of the NotificationConsumer class.
    """

    dependencies = [
        ('blog_api', '0017_post_is_post_pro'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default='posts/default.jpg', 
                                    upload_to=blog_api.models.upload_to, verbose_name='Image'),
        ),
    ]
