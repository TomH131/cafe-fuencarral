# Generated by Django 5.1.2 on 2024-11-03 18:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('people', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6')])),
                ('date', models.DateField()),
                ('time', models.TimeField(choices=[(datetime.time(17, 0), '17:00'), (datetime.time(17, 30), '17:30'), (datetime.time(18, 0), '18:00'), (datetime.time(18, 30), '18:30'), (datetime.time(19, 0), '19:00'), (datetime.time(19, 30), '19:30'), (datetime.time(20, 0), '20:00'), (datetime.time(20, 30), '20:30'), (datetime.time(21, 0), '21:00')], default=datetime.time(17, 0))),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(default='example@example.com', max_length=200)),
            ],
        ),
    ]
