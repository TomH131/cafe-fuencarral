from django.db import models
from datetime import time
from django.utils import timezone
import random
import string
from django.contrib.auth.hashers import make_password


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

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Cancelled", "Cancelled"),
    ]

    people = models.IntegerField(choices=NUMBER_OF_PEOPLE_CHOICES)
    date = models.DateField()
    time = models.TimeField(choices=TIME_OF_DAY_CHOICES)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=128)
    code = models.CharField(max_length=15, blank=True, null=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Active"
    )

    def time_submitted(self):
        # This timestamps the booking so we know when it was made
        self.timestamp = timezone.now()
        self.save()

    def __str__(self):
        # This provides a description of the reservation for the admin page
        return f"Reservation for {self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code()
        if not self.timestamp:
            self.timestamp = timezone.now()
        if not self.status:
            self.status = "Active"

        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)

        super(Reservation, self).save(*args, **kwargs)


def generate_code(length=8, prefix="FUE-"):
    # This assigns a randomly generated code to each reservation
    characters = string.ascii_uppercase + string.digits
    random_code = ''.join(random.choice(characters) for _ in range(length))
    return prefix + random_code
