# Generated by Django 4.2.11 on 2024-05-06 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wasteschedules', '0003_alter_schedule_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='created_at',
        ),
    ]
