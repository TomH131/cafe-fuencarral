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

    name = models.CharField(max_length=200)
    people = models.IntegerField(
        choices=NUMBER_OF_PEOPLE_CHOICES
    )
    date = models.DateField()
    email = models.EmailField(max_length=200)
    time = models.IntegerField()

