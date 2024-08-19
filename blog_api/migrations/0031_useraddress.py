# Generated by Django 4.2.11 on 2024-06-06 10:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog_api', '0030_notifications_to'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=200)),
                ('country', models.CharField(choices=[('azerbaijan', 'Azerbaijan'), ('bahamas', 'Bahamas'), ('bahrain', 'Bahrain'), ('bangladesh', 'Bangladesh'), ('barbados', 'Barbados')], default=None, max_length=20)),
                ('street_address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('zip_code', models.IntegerField(max_length=200)),
                ('notes', models.TextField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
