from django.db import models
from datetime import time
import random
import string

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
        (time(17, 0), "17:00"),
        (time(17, 30), "17:30"),
        (time(18, 0), "18:00"),
        (time(18, 30), "18:30"),
        (time(19, 0), "19:00"),
        (time(19, 30), "19:30"),
        (time(20, 0), "20:00"),
        (time(20, 30), "20:30"),
        (time(21, 0), "21:00"),
    ]

    SPECIAL_OCCASION_CHOICES = [
        ("None", "None"),
        ("Birthday", "Birthday"),
        ("Anniversary", "Anniversary"),
    ]

    people = models.IntegerField(choices=NUMBER_OF_PEOPLE_CHOICES)
    date = models.DateField()
    time = models.TimeField(choices=TIME_OF_DAY_CHOICES)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    special_occasion = models.CharField(
        max_length=200, 
        choices=SPECIAL_OCCASION_CHOICES, 
        blank=True)
    code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Reservation for {self.name} on {self.date.strftime('%d-%m-%Y')} at {self.time}"

    def save(self, *args, **kwargs):
        self.code = generate_code()
        super(Reservation, self).save(*args, **kwargs)

def generate_code(length=8, prefix="FUE-"):
    # Choose from uppercase letters and digits
    characters = string.ascii_uppercase + string.digits
    # Generate random characters for the specified length
    random_code = ''.join(random.choice(characters) for _ in range(length))
    # Return the code with the prefix
    return prefix + random_code