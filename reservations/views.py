from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservationPart1Form, ReservationPart2Form, SearchForm
from .models import Reservation


def reservation_step1_view(request):
    # This is the first part of the reservation submission
    if request.method == 'POST':
        form = ReservationPart1Form(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            if cleaned_data.get('date'):
                cleaned_data['date'] = cleaned_data['date'].strftime(
                        '%Y-%m-%d')

            if cleaned_data.get('time'):
                cleaned_data['time'] = cleaned_data['time'].strftime(
                        '%H:%M:%S')

            request.session['reservation_data'] = cleaned_data

            return redirect('reservations:step-two')

    else:
        form = ReservationPart1Form()

    return render(request, 'reservations/reservation_step1.html', {
        'form': form})


def reservation_step2_view(request):
    # This is the second part of the reservation submission
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

    return render(request, 'reservations/reservation_step2.html', {
        'form': form})


def submission_view(request):
    # This confirms the reservation and shows the details
    code = request.session.get('reservation_code')

    reservation = Reservation.objects.filter(
        code=code).first() if code else None

    context = {
        'code': code,
        'reservation': reservation,
    }

    return render(request, 'reservations/submission.html', context)


def search_view(request):
    # This is to search for an existing reservation using the code given
    reservations = []
    error_message = None

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            reservations = Reservation.objects.filter(code=code)

            if not reservations.exists():
                error_message = "This code does not exist. Please try again."

            else: 
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
    # This is to make any modifications to an existing reservation
    reservation = get_object_or_404(Reservation, code=code)

    if reservation.status != "Active":
        return redirect('reservations:cancel', code=code)

    if request.method == 'POST':
        form_part1 = ReservationPart1Form(request.POST, instance=reservation, current_reservation=reservation)
        form_part2 = ReservationPart2Form(request.POST, instance=reservation, is_modifying=True)

        if form_part1.is_valid() and form_part2.is_valid():
            reservation = form_part1.save(commit=False)
            form_part2_data = form_part2.cleaned_data

            # Only update the password if the user provides a new one
            if form_part2_data['password']:
                reservation.password = form_part2_data['password']

            reservation.first_name = form_part2_data['first_name']
            reservation.last_name = form_part2_data['last_name']
            reservation.email = form_part2_data['email']
            reservation.save()

            return redirect('reservations:update', code=reservation.code)

    else:
        form_part1 = ReservationPart1Form(instance=reservation, current_reservation=reservation)
        form_part2 = ReservationPart2Form(instance=reservation, is_modifying=True)

    return render(request, 'reservations/modify.html', {
        'form_part1': form_part1,
        'form_part2': form_part2,
        'reservation': reservation
    })


def cancel_view(request, code):
    # This is to cancel any reservation
    reservation = get_object_or_404(Reservation, code=code)

    if reservation.status == "Active":
        reservation.status = "Cancelled"
        reservation.save()
        return render(request, 'reservations/cancel.html', {
            'reservation': reservation})
    return redirect('reservation:details', code=reservation.code)


def details_view(request, code):
    # This shows the reservation details with the option to modify or cancel it
    reservation = get_object_or_404(Reservation, code=code)

    can_modify = reservation.status == "Active"
    can_cancel = reservation.status == "Active"

    return render(request, 'reservations/details.html', {
        'reservation': reservation,
        'can_modify': can_modify,
        'can_cancel': can_cancel
    })


def update_view(request, code):
    # This shows confirmation the reservation has been updated
    return render(request, 'reservations/update.html')
