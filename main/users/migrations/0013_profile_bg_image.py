# Generated by Django 3.2.8 on 2021-10-20 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20211017_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bg_image',
            field=models.ImageField(default='bg_default.jpg', upload_to='bg_images'),
        ),
    ]