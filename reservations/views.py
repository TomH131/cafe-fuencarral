from django.shortcuts import render, redirect
from .forms import ReservationForm, SearchForm
from .models import Reservation

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
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            reservations = Reservation.objects.filter(code=code)
    else:
        form = SearchForm()
        reservations = []

    return render(request, 'reservations/search.html', {'form': form, 'reservations': reservations})
    
