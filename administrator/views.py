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
from django.db.models import Q
from datetime import datetime
from django.core.exceptions import ValidationError
from django.http import  HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
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
    
            
            

#Forfetching the Patients data
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["GET"])
def fetch_patients(request):
    try:
        # Get query parameters
        patients_id = request.GET.get("id")
        email = request.GET.get("email")
        phone = request.GET.get("phone")
        
        # Log incoming request parameters for debugging
        logger.debug(f"Fetch patients request - ID: {patients_id}, Email: {email}, Phone: {phone}")
        
        # Start with all patients
        patients = Patients.objects.all()
        
        # Apply filters if parameters are provided
        if patients_id:
            try:
                patients_id = int(patients_id)  # Ensure ID is an integer
                patients = patients.filter(id=patients_id)
            except ValueError:
                return JsonResponse({
                    'error': 'Invalid patient ID format'
                }, status=400)
        
        if email:
            patients = patients.filter(email=email)
            
        if phone:
            patients = patients.filter(phone=phone)
            
        # Check if any patients were found
        if not patients.exists():
            return JsonResponse({
                'message': 'No patients found matching the criteria',
                'data': []
            }, status=404)
            
        # Convert queryset to list of dictionaries
        patients_data = list(patients.values(
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'address',
            'gender',
            'date_of_birth'
        ))
        
        return JsonResponse({
            'message': 'Patients retrieved successfully',
            'data': patients_data
        })
        
    except Patients.DoesNotExist:
        logger.error("Patients table does not exist")
        return JsonResponse({
            'error': 'Database table not found'
        }, status=500)
        
    except Exception as e:
        logger.error(f"An unexpected error occurred in fetch_patients: {str(e)}", exc_info=True)
        return JsonResponse({
            'error': 'An internal server error occurred'
        }, status=500)




#For deleting a patient

import logging
logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_patient(request, patient_id):
    try:
        # Log the deletion attempt
        logger.info(f"Attempting to delete patient with ID: {patient_id}")
        patient_id=int(patient_id)
        
        # Try to get the patient
        try:
            patient = Patients.objects.get(id=patient_id)
        except ObjectDoesNotExist:
            logger.warning(f"Attempted to delete non-existent patient with ID: {patient_id}")
            return JsonResponse({
                'error': 'Patient not found'
            }, status=404)
        
        #  Check for related appointments and delete them first
        related_appointments = Appointment.objects.filter(patient_id=patient_id)
        if related_appointments.exists():
            logger.info(f"Deleting {related_appointments.count()} related appointments for patient {patient_id}")
            related_appointments.delete()
        
        # Store patient info for logging
        patient_info = f"ID: {patient.id}, Name: {patient.first_name} {patient.last_name}"
        
        # Delete the patient
        patient.delete()
        
        # Log successful deletion
        logger.info(f"Successfully deleted patient - {patient_info}")
        
        return JsonResponse({
            'message': 'Patient deleted successfully',
            'patient_id': patient_id
        })
        
    except Exception as e:
        # Log the error
        logger.error(f"Error deleting patient {patient_id}: {str(e)}", exc_info=True)
        
        return JsonResponse({
            'error': 'An error occurred while deleting the patient'
        }, status=500)       





#For fetching doctors data

logger = logging.getLogger(__name__)
@csrf_exempt
@require_http_methods(["GET"])
def fetch_doctors(request):
    try:
        # Get query parameters
        doctors_id = request.GET.get("id")
        email = request.GET.get("email")
        phone = request.GET.get("phone")
        
        # Log incoming request parameters for debugging
        logger.debug(f"Fetch doctor request - ID: {doctors_id}, Email: {email}, Phone: {phone}")
        
        # Start with all doctors
        doctors = Doctors.objects.all()
        
        # Apply filters if parameters are provided
        if doctors_id:
            try:
                doctors_id = int(doctors_id)  # Ensure ID is an integer
                doctors =doctors.filter(id=doctors_id)
            except ValueError:
                return JsonResponse({
                    'error': 'Invalid doctor ID format'
                }, status=400)
        
        if email:
            doctors = doctors.filter(email=email)
            
        if phone:
            doctors = doctors.filter(phone=phone)
            
        # Check if any doctors were found
        if not doctors.exists():
            return JsonResponse({
                'message': 'No doctors found matching the criteria',
                'data': []
            }, status=404)
            
        # Convert queryset to list of dictionaries
        doctors_data = list(doctors.values(
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'specialization',
            'schedule'
        ))
        
        return JsonResponse({
            'message': 'doctors retrieved successfully',
            'data': doctors_data
        })
        
    except Doctors.DoesNotExist:
        logger.error("doctors table does not exist")
        return JsonResponse({
            'error': 'Database table not found'
        }, status=500)
        
    except Exception as e:
        logger.error(f"An unexpected error occurred in fetch_doctors: {str(e)}", exc_info=True)
        return JsonResponse({
            'error': 'An internal server error occurred'
        }, status=500)
        
        
        
        
#For deleting Doctors
import logging
logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_doctor(request, doctor_id):
    try:
        # Log the deletion attempt
        logger.info(f"Attempting to delete doctor with ID: {doctor_id}")
        doctor_id=int(doctor_id)
        
        # Try to get the doctor
        try:
            doctor = Doctors.objects.get(id=doctor_id)
        except ObjectDoesNotExist:
            logger.warning(f"Attempted to delete non-existent patient with ID: {doctor_id}")
            return JsonResponse({
                'error': 'doctor not found'
            }, status=404)
        
        #  Check for related appointments and delete them first
        related_appointments = Appointment.objects.filter(doctor_id=doctor_id)
        if related_appointments.exists():
            logger.info(f"Deleting {related_appointments.count()} related appointments for doctor {doctor_id}")
            related_appointments.delete()
        
        # Store doctor info for logging
        doctor_info = f"ID: {doctor.id}, Name: {doctor.first_name} {doctor.last_name}"
        
        # Delete the doctor
        doctor.delete()
        
        # Log successful deletion
        logger.info(f"Successfully deleted doctor - {doctor_info}")
        
        return JsonResponse({
            'message': 'Doctor deleted successfully',
            'doctor_id': doctor_id
        })
        
    except Exception as e:
        # Log the error
        logger.error(f"Error deleting doctor {doctor_id}: {str(e)}", exc_info=True)
        
        return JsonResponse({
            'error': 'An error occurred while deleting the doctor'
        }, status=500)       
