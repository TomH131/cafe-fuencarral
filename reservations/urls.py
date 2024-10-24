from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('reservations/', views.reservations_view, name='reservations'),
]
