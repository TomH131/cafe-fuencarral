from django.shortcuts import render

# Create your views here.
def reservations_view(request):
    return render(request, 'reservations/reservations.html')
