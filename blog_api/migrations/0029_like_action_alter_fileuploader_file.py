# Generated by Django 4.2.11 on 2024-05-30 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_api', '0028_alter_fileuploader_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='action',
            field=models.CharField(default='like', max_length=200),
        ),
        migrations.AlterField(
            model_name='fileuploader',
            name='file',
            field=models.FileField(upload_to='csv'),
        ),
    ]
