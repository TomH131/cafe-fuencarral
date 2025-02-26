from django import forms
from .models import Reservation
from django.core.exceptions import ValidationError
from datetime import date, datetime, timedelta
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.text import slugify


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
        cleaned_data = super().clean()
        selected_date = cleaned_data.get('date')
        selected_time = cleaned_data.get('time')

        if selected_date and selected_time:
            selected_datetime = datetime.combine(selected_date, selected_time)

            start_time = (selected_datetime - timedelta(hours=1.5)).time()
            end_time = (selected_datetime + timedelta(hours=1.5)).time()

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
        user.username = slugify(self.cleaned_data['email'].split('@')[0])  # Generate username
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autofocus': True}),
        label="Email"
    )
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    def clean(self):
        email = self.cleaned_data.get("username").lower()
        password = self.cleaned_data.get("password")

        if email and password:
            # Attempt to get the user by email (not username)
            try:
                user = authenticate(request=self.request, username=email, password=password)
            except Exception:
                user = None

            if user is None:
                raise forms.ValidationError("Invalid email or password.")
            elif not user.is_active:
                raise forms.ValidationError("This account is inactive.")
            
            self.user_cache = user

        return self.cleaned_data
