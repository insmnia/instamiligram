# Generated by Django 3.2.8 on 2021-10-15 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0009_alter_comment_options'),
        ('users', '0009_profile_saved_posts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='saved_posts',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='instagram.post'),
        ),
    ]
