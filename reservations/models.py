from django.db import models

# Create your models here.
class Reservation(models.Model):
    NUMBER_OF_PEOPLE_CHOICES = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
        (6, "6"),
    ]

    TIME_OF_DAY_CHOICES = [
        ("17:00", "17:00"),
        ("17:30", "17:30"),
        ("18:00", "18:00"),
        ("18:30", "17:30"),
        ("19:00", "19:00"),
        ("19:30", "19:30"),
        ("20:00", "20:00"),
        ("20:30", "20:30"),
        ("21:00", "21:00"),
    ]

    people = models.IntegerField(
        choices=NUMBER_OF_PEOPLE_CHOICES
    )
    date = models.DateField()
    time = models.IntegerField(
        choices=TIME_OF_DAY_CHOICES
    )
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)

