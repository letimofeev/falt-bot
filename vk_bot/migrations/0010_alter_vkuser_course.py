# Generated by Django 3.2.6 on 2021-08-17 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vk_bot', '0009_alter_vkuser_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vkuser',
            name='course',
            field=models.IntegerField(blank=True, choices=[(1, '1 курс'), (2, '2 курс'), (3, '3 курс'), (4, '4 курс')], null=True),
        ),
    ]
