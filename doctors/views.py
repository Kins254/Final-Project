from django.shortcuts import render
from django.http import HttpResponse

def say_doctor(request):
    return HttpResponse('Hello doctor')
