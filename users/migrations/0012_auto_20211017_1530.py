# Generated by Django 3.2.8 on 2021-10-17 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_profile_saved_posts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='followers_count',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='following_count',
        ),
    ]