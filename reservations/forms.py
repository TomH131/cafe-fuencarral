from django import forms
from .models import Reservation
from django.core.exceptions import ValidationError
from datetime import date, datetime, timedelta
from django.contrib.auth.models import User, AuthenticationForm

MAX_RESERVATIONS_PER_SLOT = 10


class ReservationForm(forms.ModelForm):
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
            raise ValidationError(
                    "The chosen date is in the past and cannot be used.")
        return selected_date

    def clean(self):
        # This is to stop any bookings within two hours of a fully booked time
        cleaned_data = super().clean()
        selected_date = cleaned_data.get('date')
        selected_time = cleaned_data.get('time')
        if selected_date and selected_time:
            start_time = (
                datetime.combine(selected_date, selected_time)
                - timedelta(hours=1.5)).time()
            end_time = (datetime.combine(selected_date, selected_time)
                        + timedelta(hours=1.5)).time()

            overlapping_reservations = Reservation.objects.filter(
                date=selected_date,
                time__range=(start_time, end_time),
                status="Active"
            )
            if self.current_reservation:
                overlapping_reservations = overlapping_reservations.exclude(
                    id=self.current_reservation.id)

            if overlapping_reservations.count() >= MAX_RESERVATIONS_PER_SLOT:
                raise ValidationError(
                    "All our tables are fully booked at that time. "
                    "Please select a different time."
                )

        return cleaned_data


class SearchForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Input your code'
    }))
    
    def clean_code(self):
        code = self.cleaned_data['code']
        return code.upper()


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}), label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    def clean_username(self):
        return self.cleaned_data.get("username").lower()
