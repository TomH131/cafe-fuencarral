from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'reservations'

urlpatterns = [
    path('submission/', views.submission_view, name='submission'),
    path('modify/', views.modify_view, name='modify'),
    path('cancel/', views.cancel_view, name='cancel'),
    path('details/', views.details_view, name='details'),
    path('update/', views.update_view, name='update'),
    path('', views.reservation_view, name='reservations'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
