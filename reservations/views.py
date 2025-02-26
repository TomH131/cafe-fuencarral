from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservationForm, SearchForm, SignupForm
from .models import Reservation
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("reservations:reservation")
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("reservations:reservation")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def reservation_view(request):
    # Handles both new reservations and updates
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            return redirect("reservations:details", code=reservation.code)
    else:
        form = ReservationForm()

    return render(request, "reservations/submission.html", {"form": form})


def search_view(request):
    # Search for an existing reservation using a reservation code
    reservations = []
    error_message = None

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get("code")
            reservations = Reservation.objects.filter(code=code)

            if not reservations.exists():
                error_message = "This code does not exist. Please try again."
            else:
                reservation = reservations.first()
                return redirect("reservations:details", code=reservation.code)
    else:
        form = SearchForm()

    return render(request, "reservations/search.html", {
        "form": form,
        "reservations": reservations,
        "error_message": error_message
    })


def modify_view(request, code):
    # Modify an existing reservation
    reservation = get_object_or_404(Reservation, code=code)

    if reservation.status != "Active":
        return redirect("reservations:cancel", code=code)

    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect("reservations:update", code=reservation.code)
    else:
        form = ReservationForm(instance=reservation)

    return render(request, "reservations/modify.html", {
        "form": form,
        "reservation": reservation
    })


def cancel_view(request, code):
    # Cancel a reservation
    reservation = get_object_or_404(Reservation, code=code)

    if reservation.status == "Active":
        reservation.status = "Cancelled"
        reservation.save()

    return render(request, "reservations/cancel.html", {"reservation": reservation})


def details_view(request, code):
    # Show reservation details with modification/cancellation options
    reservation = get_object_or_404(Reservation, code=code)

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
