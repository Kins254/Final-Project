from django.urls import path
from doctors import views  # Replace with your app name

urlpatterns = [
    path('doctors/', views.doctors, name='doctors'), 
    path('dashboard/',views.dashboard,name='dashboard'),
    path('account_edit/',views.account_edit,name='account_edit'),
]