# Generated by Django 3.2.6 on 2021-08-14 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vk_bot', '0002_auto_20210814_1320'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vkmessage',
            old_name='user_id',
            new_name='user',
        ),
    ]