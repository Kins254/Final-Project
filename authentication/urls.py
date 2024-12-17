from django.urls import path
from authentication import views  # Replace with your app name

urlpatterns = [
    path('signIn/', views.signIn, name='sign_in'), 
     path('signUp/', views.signUp, name='signUp'),
    # ... other URL patterns
]


