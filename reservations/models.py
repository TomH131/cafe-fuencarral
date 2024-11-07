from django.db import models
from datetime import time
from django.utils import timezone
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

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Cancelled", "Cancelled"),
    ]

    people = models.IntegerField(choices=NUMBER_OF_PEOPLE_CHOICES)
    date = models.DateField()
    time = models.TimeField(choices=TIME_OF_DAY_CHOICES)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    special_occasion = models.CharField(
        max_length=200, 
        choices=SPECIAL_OCCASION_CHOICES, 
        blank=True,
        default='None')
    code = models.CharField(max_length=20, blank=True, null=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=200,
        choices=STATUS_CHOICES,
        default="Active"
    )

    def time_submitted(self):
        self.timestamp = timezone.now()
        self.save()

    def __str__(self):
        return f"Reservation for {self.first_name} {self.last_name} on {self.date.strftime('%d-%m-%Y')} at {self.time}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code()
        
        if not self.timestamp:
            self.timestamp = timezone.now()

        if not self.status:
            self.status = "Active"
        
        super(Reservation, self).save(*args, **kwargs)

def generate_code(length=8, prefix="FUE-"):
    characters = string.ascii_uppercase + string.digits
    random_code = ''.join(random.choice(characters) for _ in range(length))
    return prefix + random_code