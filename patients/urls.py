from django.urls import path
from patients import views  # Replace with your app name

urlpatterns = [
    path('patients/', views.patients, name='patients'), 
    path('dashboard/',views.dashboard,name='dashboard'),
    path('book_appointment/',views.book_appointment,name='book_appointment'),
    path('view_appointment/<int:patient_id>/', views.view_appointment, name='view_appointment'),
    path('updating_appointment/<int:appointment_id>/',views.updating_appointment,name='updating_appointment'),
    path('delete_appointment/', views.delete_appointment, name='delete_appointment'),
    path('account_edit/',views.account_edit,name='account_edit'),
    path('delete_account/',views.delete_account,name='delete_account'),
]