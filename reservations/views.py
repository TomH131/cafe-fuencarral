from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservationForm, SignupForm
from .models import Reservation
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home:home")
    else:
        form = SignupForm()
    return render(request, "reservations/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.user_cache  # User is authenticated here
            login(request, user)
            return redirect("home:home")  # Adjust the redirect as per your needs
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()

    return render(request, 'reservations/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect("home:home")


@login_required
def reservation_view(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            return redirect("reservations:details")
    else:
        form = ReservationForm()

    return render(request, "reservations/reservation.html", {"form": form})


@login_required
def modify_view(request):
    reservations = Reservation.objects.filter(status='Active')

    if not reservations:
        return render(request, 'reservations/modify.html', {'message': 'No active reservations found.'})

    return render(request, 'reservations/modify.html', {'reservations': reservations})


@login_required
def cancel_view(request):
    reservation = get_object_or_404(Reservation, user=request.user, status="Active")

    if reservation.status == "Active":
        reservation.status = "Cancelled"
        reservation.save()

    return render(request, "reservations/cancel.html", {"reservation": reservation})


@login_required
def details_view(request):
    # Filter reservations to get active ones
    reservations = Reservation.objects.filter(status='Active')

    # If no active reservations are found, set reservation to None
    if not reservations:
        reservation = None
    elif reservations.count() == 1:
        # If there's exactly one active reservation, use it
        reservation = reservations.first()
    else:
        # If there are multiple active reservations, handle as needed
        reservation = None  # Or handle this case as needed

    # Example logic to determine whether the reservation can be modified or canceled
    can_modify = True  # Your logic here
    can_cancel = True  # Your logic here

    return render(
        request,
        'reservations/details.html',
        {
            'reservation': reservation,
            'can_modify': can_modify,
            'can_cancel': can_cancel,
        }
    )


def update_view(request):
    # Confirmation page for updated reservation
    return render(request, "reservations/update.html")


def submission_view(request):
    # Retrieve the reservation code from the session
    code = request.session.get('reservation_code')
    
    # Fetch the reservation details if the code exists
    reservation = Reservation.objects.filter(code=code).first() if code else None

    return render(request, 'reservations/submission.html', {'reservation': reservation})


def bookings_view(request):
    # Filter reservations to show only active ones for the current user
    reservations = Reservation.objects.filter(status='Active')  # Modify this query if needed (e.g., based on user or other filters)
    
    return render(request, 'reservations/bookings.html', {'reservations': reservations})