from django.urls import path
from . import views

app_name = 'reservation'

urlpatterns = [
    path('', views.reservations_view, name='reservations'),
    path('submission/', views.submission_view, name='submission'),
    path('search/', views.search_view, name='search'),
    path('modify/<str:code>/', views.modify_view, name='modify'),
    path('cancel/<str:code>/', views.cancel_view, name='cancel'),
]
