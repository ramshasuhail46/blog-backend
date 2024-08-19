# Generated by Django 4.0.3 on 2024-03-11 07:17
"""
Connect method docstring: Brief description of the connect method.
"""
from django.db import migrations, models


class Migration(migrations.Migration):
    """
Connect method docstring: Brief description of the connect method.
"""

    dependencies = [
        ('users', '0002_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
