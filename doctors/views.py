from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render

def doctors(request):
   return render(request, 'doctor/doctors.html')


#For Log In
from django.shortcuts import render,redirect

def dashboard(request):
    user_id = request.session.get('user_id')  # Retrieve the user ID from the session
    if not user_id:
        return redirect('authentication:login')  # Redirect to login if no user ID in session

    # Fetch additional patient details if needed
    return render(request, "doctor/doctors.html", {"user_id": user_id})
