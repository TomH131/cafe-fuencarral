from django import forms
from .models import Reservation
from django.core.exceptions import ValidationError
from datetime import date

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['people', 'date', 'time', 'name', 'email', 'special_occasion']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def clean_date(self):
        selected_date = self.cleaned_data['date']
        if selected_date < date.today():
            raise ValidationError("This date is in the past and cannot be selected")
        return selected_date

class SearchForm(forms.Form):
    code = forms.CharField() 