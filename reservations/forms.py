from django import forms
from .models import Reservation
from django.core.exceptions import ValidationError
from datetime import date

MAX_RESERVATIONS_PER_SLOT = 10

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['people', 'date', 'time', 'first_name', 'last_name', 'email']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def clean_date(self):
        selected_date = self.cleaned_data['date']
        if selected_date < date.today():
            raise ValidationError("This date is in the past and cannot be selected")
        return selected_date

    def clean(self):
        cleaned_data = super().clean()
        selected_date = cleaned_data.get('date')
        selected_time = cleaned_data.get('time')
    
        if selected_date and selected_time:
            formatted_date = selected_date.strftime('%d/%m/%Y')
            
            formatted_time = selected_time.strftime('%H:%M')
            
            formatted_time = formatted_time.zfill(5)
            
            existing_reservations = Reservation.objects.filter(
                date=selected_date,
                time=selected_time
            ).count()
        
            if existing_reservations >= MAX_RESERVATIONS_PER_SLOT:
                raise ValidationError(
                    f"Sorry, all tables are booked for {formatted_date} at {formatted_time}. Please select a different time or date."
                )
    
        return cleaned_data

class SearchForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Input your code'}))