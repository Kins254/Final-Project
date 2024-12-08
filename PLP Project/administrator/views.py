from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# administrator/views.py
from django.http import HttpResponse

def home(request):
    return HttpResponse("Administrator home page")


