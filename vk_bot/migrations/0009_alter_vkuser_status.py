# Generated by Django 3.2.6 on 2021-08-14 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vk_bot', '0008_auto_20210815_0006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vkuser',
            name='status',
            field=models.CharField(choices=[('reg1', 'Course registration'), ('reg2', 'Group registration'), ('any', 'Available for any function'), ('link', 'Links to classes'), ('sch', 'Schedule')], default='any', max_length=4),
        ),
    ]
