# Generated by Django 4.2.11 on 2024-05-29 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_api', '0024_remove_post_likes_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ecommerce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('iban', models.CharField(max_length=200)),
                ('quantity_in_stock', models.IntegerField()),
                ('product_price', models.FloatField()),
                ('product_category', models.CharField(max_length=200)),
                ('product_brand', models.CharField(max_length=200)),
                ('product_rating', models.FloatField()),
            ],
        ),
    ]
