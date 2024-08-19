# Generated by Django 4.0.3 on 2024-03-11 13:13
"""
Connect method docstring: Brief description of the connect method.
"""
from django.db import migrations, models


class Migration(migrations.Migration):
    """
Connect method docstring: Brief description of the connect method.
"""

    dependencies = [
        ('users', '0005_alter_user_is_superuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
