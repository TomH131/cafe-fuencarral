from django import forms
from .models import Reservation
from django.core.exceptions import ValidationError
from datetime import date, datetime, timedelta

MAX_RESERVATIONS_PER_SLOT = 10

class ReservationPart1Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.current_reservation = kwargs.pop('current_reservation', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Reservation
        fields = ['people', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_date(self):
        selected_date = self.cleaned_data['date']
        if selected_date < date.today():
            raise ValidationError("The chosen date is in the past and cannot be used.")
        return selected_date

    
    def clean(self):
        # This is to stop any bookings within two hours of a fully booked time
        cleaned_data = super().clean()
        selected_date = cleaned_data.get('date')
        selected_time = cleaned_data.get('time')
    
        if selected_date and selected_time:
            start_time = (datetime.combine(selected_date, selected_time) - timedelta(hours=1.5)).time()
            end_time = (datetime.combine(selected_date, selected_time) + timedelta(hours=1.5)).time()
            
            overlapping_reservations = Reservation.objects.filter(
                date=selected_date,
                time__range=(start_time, end_time)
            )
            if self.current_reservation:
                overlapping_reservations = overlapping_reservations.exclude(id=self.current_reservation.id)

            if overlapping_reservations.count() >= MAX_RESERVATIONS_PER_SLOT:
                formatted_date = selected_date.strftime('%d/%m/%Y')
                formatted_time = selected_time.strftime('%H:%M')
                raise ValidationError(
                    "All our tables are fully booked at that time. Please select a different time."
                )
    
        return cleaned_data

class ReservationPart2Form(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

class SearchForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Input your code'}))