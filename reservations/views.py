from django.shortcuts import render
from reservations.models import Reservation

# Create your views here.
def reservations_view(request):
    return render(request, 'reservations/reservations.html')

def Reservation(request):
    class Meta:
        model = Booking
        fields = ['name', 'people', 'date']
