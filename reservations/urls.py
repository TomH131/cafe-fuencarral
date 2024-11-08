from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('submission/', views.submission_view, name='submission'),
    path('search/', views.search_view, name='search'),
    path('modify/<str:code>/', views.modify_view, name='modify'),
    path('cancel/<str:code>/', views.cancel_view, name='cancel'),
    path('details/<str:code>/', views.details_view, name='details'),
    path('update/<str:code>/', views.update_view, name='update'),
    path('', views.reservations_view, name='reservations'),
]
