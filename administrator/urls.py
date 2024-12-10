# administrator/urls.py
from django.urls import path
from . import views  # Make sure you have views set up

urlpatterns = [
    path('', views.home, name='admin_home'),  # Replace with your actual views
]
