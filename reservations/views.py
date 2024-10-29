from django.shortcuts import render, redirect
from .forms import ReservationForm

def reservations_view(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new reservation to the database
            return redirect('reservations_view')  # Redirect to the same page
    else:
        form = ReservationForm()
    
    return render(request, 'reservations/reservations.html', {'form': form})
