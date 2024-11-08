from django.urls import path
from . import views

app_name = 'reservation'

urlpatterns = [
    path('submission/', views.submission_view, name='submission'),
    path('search/', views.search_view, name='search'),
    path('modify/<str:code>/', views.modify_view, name='modify'),
    path('cancel/<str:code>/', views.cancel_view, name='cancel'),
    path('details/<str:code>/', views.details_view, name='details'),
    path('update/<str:code>/', views.update_view, name='update'),
    path('step-one/', views.reservation_step_one_view, name='step_one'),
    path('step-two/', views.reservation_step_two_view, name='step_two'),
]
