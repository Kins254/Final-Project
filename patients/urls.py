from django.urls import path
from patients import views  # Replace with your app name

urlpatterns = [
    path('patients/', views.patients, name='patients'), 
    path('dashboard/',views.dashboard,name='dashboard'),
    path('book_appointment/',views.book_appointment,name='book_appointment'),
    #path('view_appointment/<int:patient_id>/', views.view_appointment, name='view_appointment'),
    
]