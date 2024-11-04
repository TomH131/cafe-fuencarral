from django.shortcuts import render, redirect
from .forms import ReservationForm

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
