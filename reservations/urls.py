from django.urls import path
from . import views

app_name = 'reservation'

urlpatterns = [
    path('', views.reservations_view, name='reservations'),
    path('submission/', views.submission_view, name='submission'),
]
