# Generated by Django 4.1.2 on 2022-12-09 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_likes_liked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likes',
            name='liked',
        ),
    ]