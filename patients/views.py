from django.shortcuts import render
from django.http import HttpResponse

def say_patient(request):
    return HttpResponse('Hello patient')
