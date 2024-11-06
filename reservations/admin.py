from django.contrib import admin
from .models import Reservation

# Register your models here.
class ReservationAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Contact Information", {"fields": ["name", "email"]}),
        ("Reservation", {"fields": ["date", "time", "people", "code"]})
    ]

    list_display = ["date", "time", "people", "name"]

    list_filter = ["date"]

    # ordering = ["date", "time"]

admin.site.register(Reservation, ReservationAdmin)
