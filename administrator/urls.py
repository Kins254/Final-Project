from django.urls import path
from administrator import views  # Replace with your app name

urlpatterns = [
    
     path('dashboard/', views.dashboard, name='dashboard'),
     path('doctor_account/',views.doctor_account,name='doctor_account'),
    # ... other URL patterns
]