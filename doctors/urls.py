from django.urls import path
from doctors import views  # Replace with your app name

urlpatterns = [
    path('doctors/', views.doctors, name='doctors'), 
    path('dashboard/',views.dashboard,name='dashboard'),
    path('account_edit/',views.account_edit,name='account_edit'),
    path('view_appointment/',views.view_appointment,name='view_appointment'),
    path('approve_appointment/<int:appointment_id>/',views.approve_appointment, name='approve_appointment'),
    path('complete_appointment/<int:appointment_id>/',views.complete_appointment, name='complete_appointment'),
    path('delete_appointment/<int:appointment_id>/',views.delete_appointment, name='delete_appointment'),
    path('delete_account/',views.delete_account,name='delete_account'),



]