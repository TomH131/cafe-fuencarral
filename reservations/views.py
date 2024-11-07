from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservationForm, SearchForm
from .models import Reservation
from django.urls import reverse

def reservations_view(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            request.session['reservation_code'] = reservation.code
            return redirect('reservation:submission')
    else:
        form = ReservationForm()
    
    return render(request, 'reservations/reservations.html', {'form': form})

def submission_view(request):
    code = request.session.get('reservation_code')
    
    if code:
        del request.session['reservation_code']

    return render(request, 'reservations/submission.html', {'code': code})

def search_view(request):
    reservations = []
    error_message = None

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            reservations = Reservation.objects.filter(code=code)
            
            if not reservations.exists():
                error_message = "This code does not exist."

            if reservations.exists():
                return redirect('reservation:modify', code=code)
    else:
        form = SearchForm()

    return render(request, 'reservations/search.html', {'form': form, 'reservations': reservations, 'error_message': error_message})
    
def modify_view(request, code):
    reservation = get_object_or_404(Reservation, code=code)

    return render(request, 'reservations/modify.html', {'reservation': reservation})

def cancel_view(request, code):
    reservation = get_object_or_404(Reservation, code=code)

    if reservation.status == "Active":
        reservation.status = "Cancelled"
        reservation.save()
    
    return render(request, 'reservations/cancel.html', {'reservation': reservation})