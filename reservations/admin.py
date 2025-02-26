from django.contrib import admin
from .models import Reservation

class ReservationAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Contact Information", {"fields": ["user"]}),  # Use "user" instead of individual fields
        ("Reservation", {"fields": ["date", "time", "people", "code", "status"]}),
    ]

    list_display = [
        "date", "time", "people", "get_first_name", "get_last_name", "timestamp", "status"
    ]

    list_filter = ["date", "status"]
    ordering = ["date", "time"]

    search_fields = ["user__first_name", "user__last_name", "user__email", "code"]

    def get_first_name(self, obj):
        return obj.user.first_name if obj.user else "-"
    
    def get_last_name(self, obj):
        return obj.user.last_name if obj.user else "-"

    get_first_name.admin_order_field = "user__first_name"
    get_last_name.admin_order_field = "user__last_name"
    get_first_name.short_description = "First Name"
    get_last_name.short_description = "Last Name"

admin.site.register(Reservation, ReservationAdmin)
