from django import forms
from .models import Reservation
from django.core.exceptions import ValidationError
from datetime import date, datetime, timedelta

MAX_RESERVATIONS_PER_SLOT = 10

class ReservationPart1Form(forms.ModelForm):
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
        cleaned_data = super().clean()
        selected_date = cleaned_data.get('date')
        selected_time = cleaned_data.get('time')
    
        if selected_date and selected_time:
            start_time = (datetime.combine(selected_date, selected_time) - timedelta(hours=1.5)).time()
            end_time = (datetime.combine(selected_date, selected_time) + timedelta(hours=1.5)).time()
            
            overlapping_reservations = Reservation.objects.filter(
                date=selected_date,
                time__range=(start_time, end_time)
            ).count()

            if overlapping_reservations >= MAX_RESERVATIONS_PER_SLOT:
                formatted_date = selected_date.strftime('%d/%m/%Y')
                formatted_time = selected_time.strftime('%H:%M')
                raise ValidationError("All our tables are booked. Please select a different time or date.")
    
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