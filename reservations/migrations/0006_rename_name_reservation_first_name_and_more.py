# Generated by Django 5.1.2 on 2024-11-07 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0005_reservation_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='reservation',
            name='last_name',
            field=models.CharField(default='Hill', max_length=200),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='special_occasion',
            field=models.CharField(blank=True, choices=[('None', 'None'), ('Birthday', 'Birthday'), ('Anniversary', 'Anniversary')], default='None', max_length=200),
        ),
    ]
