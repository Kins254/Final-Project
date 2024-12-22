import json
import bcrypt
import logging
from django.urls import reverse
from Base.models import Doctors
from Base.models import Patients
from Base.models import Appointment
from django.db import transaction
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import  HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

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




#For the account edit section

logger = logging.getLogger(__name__)
@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def account_edit(request):
    print(f"Received request: {request.method}")
    try:
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        newpassword = data.get("newpassword")
        userId = data.get("userId")

        if not all([email, password, newpassword, userId]):
            return JsonResponse({
                'success': False,
                'message': 'Please fill all the required fields'
            }, status=400)

        # Retrieve the user by userId 
        try:
            user = Doctors.objects.get(id=userId)
        except Doctors.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'No user found with this userId'
            }, status=404)

        # Verify the current password
        stored_hash = user.password_hash.encode('utf-8')
        input_password = password.encode('utf-8')

        if not bcrypt.checkpw(input_password, stored_hash):
            return JsonResponse({
                'success': False,
                'message': 'Incorrect password'
            }, status=401)

        # Update the email and password if provided
        if newpassword:
            new_password_hash = bcrypt.hashpw(newpassword.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user.password_hash = new_password_hash
        if 'email' in data:
            user.email = data['email']

        # Save the updates atomically
        with transaction.atomic():
            user.save()

        logger.info(f"User {userId} updated successfully")
        return JsonResponse({
            'success': True,
            'message': 'Account updated successfully'
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while updating the account'
        }, status=500)
