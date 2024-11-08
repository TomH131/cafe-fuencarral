from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservationForm, SearchForm
from .models import Reservation

def reservation_step_one_view(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        # Limit validation to fields needed in step one
        if form.is_valid():
            # Store only first-step data in session
            request.session['form_data'] = {key: form.cleaned_data[key] for key in ['people', 'date', 'time']}
            return redirect('reservation:step_two')
    else:
        form = ReservationForm()

    return render(request, 'reservations/reservation_step_one.html', {'form': form})


def reservation_step_two_view(request):
    form_data = request.session.get('form_data')
    # if not form_data:
    #     return redirect('reservation:step_one')

    if request.method == "POST":
        # Create form instance with initial data for both steps
        form = ReservationForm(request.POST, initial=form_data)
        if form.is_valid():
            # Save the reservation data
            form.save()
            return redirect('reservation:submission')
    else:
        form = ReservationForm(initial=form_data)

    return render(request, 'reservations/reservation_step_two.html', {'form': form})

def submission_view(request):
    code = request.session.get('reservation_code')
    
    if code:
        del request.session['reservation_code']

    return render(request, 'reservations/submission.html', {'code': code})

def search_view(request):
    reservations = []
    error_message = None  # Initialize error message to None

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            reservations = Reservation.objects.filter(code=code)
            
            # Check if no reservation was found
            if not reservations.exists():
                error_message = "This code does not exist."  # Set error message

            # If a reservation is found, redirect to details page
            if reservations.exists():
                reservation = reservations.first()
                return redirect('reservation:details', code=reservation.code)

    else:
        form = SearchForm()

    return render(request, 'reservations/search.html', {'form': form, 'reservations': reservations, 'error_message': error_message})
    
def modify_view(request, code):
    reservation = get_object_or_404(Reservation, code=code)

    if reservation.status != "Active":
        return redirect('reservation:cancel', code=code)

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('reservation:update', code=reservation.code)
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'reservations/modify.html', {'form': form, 'reservation': reservation})

def cancel_view(request, code):
    reservation = get_object_or_404(Reservation, code=code)

    if reservation.status == "Active":
        reservation.status = "Cancelled"
        reservation.save()
        return render(request, 'reservations/cancel.html', {'reservation': reservation})
    
    return redirect('reservation:details', code=reservation.code)

def details_view(request, code):
    reservation = get_object_or_404(Reservation, code=code)

    # Check if the status is Active
    can_modify = reservation.status == "Active"
    can_cancel = reservation.status == "Active"

    return render(request, 'reservations/details.html', {
        'reservation': reservation,
        'can_modify': can_modify,
        'can_cancel': can_cancel
    })

def update_view(request, code):
    return render(request, 'reservations/update.html')