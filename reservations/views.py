from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservationPart1Form, ReservationPart2Form, SearchForm
from .models import Reservation
from django.http import HttpResponse, JsonResponse
from datetime import datetime, date, time

# def reservations_view(request):
#     if request.method == 'POST':
#         form = ReservationForm(request.POST)
#         if form.is_valid():
#             reservation = form.save()
#             return render(request, 'reservations/submission.html', {'code': reservation.code})
#     else:
#         form = ReservationForm()

#     return render(request, 'reservations/reservations.html', {'form': form})

# def submission_view(request):
#     code = request.session.get('reservation_code')
    
#     if code:
#         del request.session['reservation_code']

#     return render(request, 'reservations/submission.html', {'code': code})

def reservation_step1_view(request):
    if request.method == 'POST':
        form = ReservationPart1Form(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            if cleaned_data.get('date'):
                cleaned_data['date'] = cleaned_data['date'].strftime('%Y-%m-%d')

            if cleaned_data.get('time'):
                cleaned_data['time'] = cleaned_data['time'].strftime('%H:%M:%S')

            request.session['reservation_data'] = cleaned_data

            return redirect('reservations:step-two')

    else:
        form = ReservationPart1Form()

    return render(request, 'reservations/reservation_step1.html', {'form': form})

def reservation_step2_view(request):
    reservation_data = request.session.get('reservation_data', {})

    if request.method == 'POST':
        form = ReservationPart2Form(request.POST)
        if form.is_valid():
            reservation_data.update(form.cleaned_data)
            
            reservation = Reservation.objects.create(
                people=reservation_data['people'],
                date=reservation_data['date'],
                time=reservation_data['time'],
                first_name=reservation_data['first_name'],
                last_name=reservation_data['last_name'],
                email=reservation_data['email']
            )

            del request.session['reservation_data']

            request.session['reservation_code'] = reservation.code

            return redirect('reservations:submission')
    else:
        form = ReservationPart2Form()

    return render(request, 'reservations/reservation_step2.html', {'form': form})


def submission_view(request):
    code = request.session.get('reservation_code')

    if code:
        del request.session['reservation_code']

        return render(request, 'reservations/submission.html', {'code': code})

    return redirect('reservations:reservations')

def search_view(request):
    reservations = []
    error_message = None

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            reservations = Reservation.objects.filter(code=code)

            if not reservations.exists():
                error_message = "This code does not exist. Please try again."

            elif reservations.exists():
                reservation = reservations.first()
                return redirect('reservations:details', code=reservation.code)

    else:
        form = SearchForm()

    return render(request, 'reservations/search.html', {
        'form': form,
        'reservations': reservations,
        'error_message': error_message
    })
    
def modify_view(request, code):
    reservation = get_object_or_404(Reservation, code=code)

    if reservation.status != "Active":
        return redirect('reservations:cancel', code=code)

    if request.method == 'POST':
        form_part1 = ReservationPart1Form(request.POST, initial={
            'people': reservation.people,
            'date': reservation.date,
            'time': reservation.time
        })
        form_part2 = ReservationPart2Form(request.POST, initial={
            'first_name': reservation.first_name,
            'last_name': reservation.last_name,
            'email': reservation.email
        })

        if form_part1.is_valid() and form_part2.is_valid():
            reservation.people = form_part1.cleaned_data['people']
            reservation.date = form_part1.cleaned_data['date']
            reservation.time = form_part1.cleaned_data['time']
            
            reservation.first_name = form_part2.cleaned_data['first_name']
            reservation.last_name = form_part2.cleaned_data['last_name']
            reservation.email = form_part2.cleaned_data['email']
            
            reservation.save()

            return redirect('reservations:update', code=reservation.code)

    else:
        form_part1 = ReservationPart1Form(initial={
            'people': reservation.people,
            'date': reservation.date,
            'time': reservation.time
        })
        form_part2 = ReservationPart2Form(initial={
            'first_name': reservation.first_name,
            'last_name': reservation.last_name,
            'email': reservation.email
        })

    return render(request, 'reservations/modify.html', {
        'form_part1': form_part1,
        'form_part2': form_part2,
        'reservation': reservation
    })

def cancel_view(request, code):
    reservation = get_object_or_404(Reservation, code=code)

    if reservation.status == "Active":
        reservation.status = "Cancelled"
        reservation.save()
        return render(request, 'reservations/cancel.html', {'reservation': reservation})
    
    return redirect('reservation:details', code=reservation.code)

def details_view(request, code):
    reservation = get_object_or_404(Reservation, code=code)

    can_modify = reservation.status == "Active"
    can_cancel = reservation.status == "Active"

    return render(request, 'reservations/details.html', {
        'reservation': reservation,
        'can_modify': can_modify,
        'can_cancel': can_cancel
    })

def update_view(request, code):
    return render(request, 'reservations/update.html')