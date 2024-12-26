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



#For Log In
from django.shortcuts import render,redirect

def dashboard(request):
    user_id = request.session.get('user_id')  # Retrieve the user ID from the session
    if not user_id:
        return redirect('authentication:login')  # Redirect to login if no user ID in session

    # Fetch additional patient details if needed
    return render(request, "administrators/administrators.html", {"user_id": user_id})


#For Creating the doctor's account
logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST"])
def doctor_account(request):
    try:
      
        # Parse JSON data
        data = json.loads(request.body)
        
        # Extract and validate fields
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        phone = data.get("phone")
        specialization = data.get("specialization")
        schedule = data.get("schedule")
        password = data.get("password")
        
     
        
        # Validate required fields
        required_fields = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'specialization': specialization,
            'schedule': schedule,
            'password': password
        }
        
        missing_fields = [field for field, value in required_fields.items() if not value]
        if missing_fields:
            logger.error(f"Missing required fields: {missing_fields}")
            return JsonResponse({
                'success': False,
                'message': f"Missing required fields: {', '.join(missing_fields)}"
            }, status=400)
        
        # Check if email exists
        if Doctors.objects.filter(email=email).exists():
            logger.warning(f"Email already exists: {email}")
            return JsonResponse({
                'success': False,
                'message': "Email already exists"
            }, status=400)
            
        # Hash password
        try:
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        except Exception as e:
            logger.error(f"Password hashing failed: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': "Password processing failed"
            }, status=500)
        
        # Create doctor record
        try:
            doctor = Doctors.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                specialization=specialization,
                schedule=schedule,
                password_hash=password_hash.decode('utf-8')
            )
            
            # Verify the doctor was created
            if doctor.id:
                logger.info(f"Doctor created with ID: {doctor.id}")
            
            return JsonResponse({
                'success': True,
                'message': 'Registration successful!',
                'doctor_id': doctor.id,
                'redirect_url': '/patients/dashboard/'
            }, status=201)

        except Exception as e:
            logger.error(f"Database creation failed with error: {str(e)}")
            # Log the full exception traceback
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return JsonResponse({
                'success': False,
                'message': f'Registration failed: {str(e)}'
            }, status=500)

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        logger.error(f"Raw request body: {request.body}")
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return JsonResponse({
            'success': False,
            'message': f'An unexpected error occurred: {str(e)}'
        }, status=500)
    
            
           
