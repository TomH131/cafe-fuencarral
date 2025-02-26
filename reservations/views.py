from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservationForm, SignupForm
from .models import Reservation
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


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
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home:home")
    else:
        form = AuthenticationForm()
    return render(request, 'reservations/login.html', {'form': form})


def logout_view(request):
    # Log the user out
    logout(request)
    
    return render(request, 'reservations/logout.html')


def reservation_view(request):
    # Handles both new reservations and updates
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("reservations:details")
    else:
        form = ReservationForm()

    return render(request, "reservations/reservation.html", {"form": form})


@login_required
def modify_view(request):
    # Try to get the reservation associated with the logged-in user
    reservation = get_object_or_404(Reservation, user=request.user)

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        
        if form.is_valid():
            form.save()
            return redirect('reservations:reservation')
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'reservations/modify.html', {'form': form, 'reservation': reservation})


def cancel_view(request):
    reservation = get_object_or_404(Reservation, user=request.user, status="Active")

    if reservation.status == "Active":
        reservation.status = "Cancelled"
        reservation.save()

    return render(request, "reservations/cancel.html", {"reservation": reservation})


def details_view(request):
    reservation = Reservation.objects.first()  

    can_modify = reservation.status == "Active"
    can_cancel = reservation.status == "Active"

    return render(request, "reservations/details.html", {
        "reservation": reservation,
        "can_modify": can_modify,
        "can_cancel": can_cancel
    })


def update_view(request, code):
    # Confirmation page for updated reservation
    return render(request, "reservations/update.html")


def submission_view(request):
    # Retrieve the reservation code from the session
    code = request.session.get('reservation_code')
    
    # Fetch the reservation details if the code exists
    reservation = Reservation.objects.filter(code=code).first() if code else None

    return render(request, 'reservations/submission.html', {'reservation': reservation})
