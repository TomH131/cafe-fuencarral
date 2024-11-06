from django.shortcuts import render, redirect
from .forms import ReservationForm, SearchForm
from .models import Reservation

def reservations_view(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservation:submission')
    else:
        form = ReservationForm()
    
    return render(request, 'reservations/reservations.html', {'form': form})

def submission_view(request):
    return render(request, 'reservations/submission.html')

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
    
