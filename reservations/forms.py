from django import forms
from .models import Reservation
from django.core.exceptions import ValidationError
from datetime import date, datetime, timedelta
from django.contrib.auth.hashers import make_password

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


class ReservationPart2Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Use the is_modifying flag to control if password is optional
        self.is_modifying = kwargs.pop('is_modifying', False)
        super().__init__(*args, **kwargs)

        if self.is_modifying:
            self.fields['password'].required = False  # Make password optional when modifying

    class Meta:
        model = Reservation
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            first_name = first_name.title()
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            last_name = last_name.title()
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower()  # Always store email in lowercase for consistency
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            # Hash the password before saving, only if it is not empty
            return make_password(password)
        return None  # Return None if password is not set or empty


class SearchForm(forms.Form):
    email = forms.EmailField(required=True, label='Email')
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Password')
    code = forms.CharField(max_length=64, required=True, label='Reservation Code')

    def clean_code(self):
        code = self.cleaned_data['code']
        # Check if the code exists in the database
        if not Reservation.objects.filter(code=code).exists():
            raise forms.ValidationError("This code does not exist.")
        return code

    def clean_email(self):
        email = self.cleaned_data['email']
        # Normalize the email to lowercase
        return email.lower()

    def clean_password(self):
        # No changes needed for the password, return it as-is
        return self.cleaned_data['password']
