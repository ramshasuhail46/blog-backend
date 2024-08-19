# Generated by Django 4.2.11 on 2024-03-14 10:02
"""
    Connect method docstring: Brief description of the connect method.
    """
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Connect method docstring: Brief description of the connect method.
    """

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                                            primary_key=True, serialize=False,
                                              verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField()),
            ],
        ),
    ]
