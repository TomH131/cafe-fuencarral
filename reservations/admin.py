from django.contrib import admin
from .models import Reservation
from django.contrib.auth.hashers import make_password


class ReservationAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Contact Information",
            {"fields": ["first_name", "last_name", "email", "password"]}),
        ("Reservation",
            {"fields": ["date", "time", "people", "code", "status"]})
    ]

    list_display = [
        "date", "time", "people", "first_name", "last_name", "timestamp",
        "status"]

    list_filter = ["date", "status"]

    ordering = ["date", "time"]

    def save_model(self, request, obj, form, change):
        # Hash the password before saving if it is not empty
        if obj.password and not obj.password.startswith('pbkdf2_sha256$'):
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)


admin.site.register(Reservation, ReservationAdmin)
