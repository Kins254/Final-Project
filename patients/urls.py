from django.urls import path
from patients import views  # Replace with your app name

urlpatterns = [
    path('patients/', views.patients, name='patients'), 
    path('dashboard/',views.dashboard,name='dashboard'),
    # ... other URL patterns
]