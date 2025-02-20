# Generated by Django 5.1.2 on 2024-11-08 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0008_remove_reservation_special_occasion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='code',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='email',
            field=models.EmailField(max_length=50),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='first_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='last_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Cancelled', 'Cancelled')], default='Active', max_length=20),
        ),
    ]
