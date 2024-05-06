# Generated by Django 4.2.11 on 2024-05-06 10:35

from django.db import migrations, models
import wasteschedules.models


class Migration(migrations.Migration):

    dependencies = [
        ('wasteschedules', '0004_remove_location_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostalCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postal_code', models.CharField(unique=True, validators=[wasteschedules.models.validate_postal_code])),
            ],
        ),
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.AlterField(
            model_name='schedule',
            name='locations',
            field=models.ManyToManyField(related_name='schedules', to='wasteschedules.postalcode'),
        ),
    ]
