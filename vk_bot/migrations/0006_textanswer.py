# Generated by Django 3.2.6 on 2021-08-14 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vk_bot', '0005_alter_vkuser_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
