# Generated by Django 5.1.2 on 2025-02-26 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0010_remove_reservation_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='password',
            field=models.CharField(default='defaultpassword', max_length=25),
        ),
    ]
