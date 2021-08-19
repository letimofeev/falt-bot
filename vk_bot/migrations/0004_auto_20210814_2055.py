# Generated by Django 3.2.6 on 2021-08-14 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vk_bot', '0003_rename_user_id_vkmessage_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='vkuser',
            name='status',
            field=models.CharField(blank=True, default='any', max_length=16),
        ),
        migrations.AlterField(
            model_name='vkuser',
            name='course',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vkuser',
            name='group',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]