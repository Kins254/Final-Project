from django.urls import path
from administrator import views  # Replace with your app name

urlpatterns = [
    
     path('dashboard/', views.dashboard, name='dashboard'),
    # ... other URL patterns
]