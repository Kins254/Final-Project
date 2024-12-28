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








#Fetching Appointments section
import logging
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["GET"])
def view_appointments(request):  # Fixed function name spelling
    try:
        # Get query parameters with correct names
        appointment_id = request.GET.get("id")  # Changed from id3
        doctor_id = request.GET.get("doctor_id")  # Changed from doctorID
        patient_id = request.GET.get("patient_id")  # Changed from patientID
        
        # Log incoming request parameters
        logger.debug(f"Fetch appointments request - ID: {appointment_id}, Doctor ID: {doctor_id}, Patient ID: {patient_id}")
        
        # Start with all appointments
        appointments = Appointment.objects.all()
        
        # Apply filters if parameters are provided
        if appointment_id:
            try:
                appointment_id = int(appointment_id)
                appointments = appointments.filter(id=appointment_id)  # Fixed variable name
            except ValueError:
                return JsonResponse({
                    'error': 'Invalid appointment ID format'
                }, status=400)
                
        if doctor_id:
            try:
                doctor_id = int(doctor_id)
                appointments = appointments.filter(doctor_id=doctor_id)  # Fixed variable name
            except ValueError:
                return JsonResponse({
                    'error': 'Invalid doctor ID format'
                }, status=400)
                        
        if patient_id:
            try:
                patient_id = int(patient_id)
                appointments = appointments.filter(patient_id=patient_id)  # Fixed variable name
            except ValueError:
                return JsonResponse({
                    'error': 'Invalid patient ID format'
                }, status=400)
            
        # Check if any appointments were found
        if not appointments.exists():
            return JsonResponse({
                'message': 'No appointments found matching the criteria',
                'data': []
            }, status=404)
            
        # Converting queryset to list of dictionaries
        appointments_data = list(appointments.values(  # Fixed variable name
            'id',
            'patient_id',
            'doctor_id',
            'appointment_date',
            'appointment_time',
            'appointment_type',
            'communication_type',
            'payment_type'
        ))
        
        return JsonResponse({
            'message': 'Appointments retrieved successfully',
            'data': appointments_data
        })
        
    except Appointment.DoesNotExist:
        logger.error("Appointments table does not exist")
        return JsonResponse({
            'error': 'Database table not found'
        }, status=500)
        
    except Exception as e:
        logger.error(f"An unexpected error occurred in fetching appointments: {str(e)}", exc_info=True)
        return JsonResponse({
            'error': 'An internal server error occurred'
        }, status=500)
        
        
 
#The Dashboard section
# Overall statistics
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def overall_stats(request):
   
    try:
        stats = {
            "total_patients": Patients.objects.all().count(),
            "total_doctors": Doctors.objects.all().count(),
            "total_appointments": Appointment.objects.all().count(),
            "pending_appointments": Appointment.objects.filter(status="Pending").count(),
            "completed_appointments": Appointment.objects.filter(status="Completed").count()
        }
        
        return JsonResponse(stats)
    except Exception as e:
        print(f"Error in stats view: {e}")  # Debug print
        return JsonResponse({"error": str(e)}, status=500)
 
 
 
 
 
 #Gender pie chart
from django.http import JsonResponse
from django.db.models import Count

def gender_pieChart(request):
    # Aggregating patient gender counts
    gender_stats = Patients.objects.values('gender').annotate(count=Count('gender'))

    # Initialize counts
    male_count = 0
    female_count = 0

    # Extract counts for each gender
    for item in gender_stats:
        if item['gender'] == 'Male':
            male_count = item['count']
        elif item['gender'] == 'Female':
            female_count = item['count']

    # Return the data as JSON
    data = {
        "male": male_count,
        "female": female_count
    }
    return JsonResponse(data)
 
 
 

 
 
 
#For Doctors specialization
 
def doctor_specialization(request):
     #Aggregating doctor specialization counts
     specialization_stats=Doctors.objects.values('specialization').annotate(count=Count('specialization'))
     
     #Initiate counts
     general_count=0
     pediatric_count=0
     dermatology_count=0
     emergency_count=0
     nutrition_and_dietetic_count=0
     infectious_disease_count=0
     
     #Extract counts for each specialization
     for item in specialization_stats:
         if item['specialization']=='General':
             general_count=item['count']
         if item['specialization']=='Pediatric':
             pediatric_count=item['count'] 
         if item['specialization']=='Dermotology':
             dermatology_count=item['count']
         if item['specialization']=='Emergency':
             emergency_count=item['count']
         if item['specialization']=='Nutrition and Dietietic':
             nutrition_and_dietetic_count=item['count']
         if item['specialization']=='Infectious Disease':
             infectious_disease_count=item['count']                  
     
     #Return as JSON file
     data={
            "General":general_count,
            "Pediatric":pediatric_count,
            "Dermotology":dermatology_count,
            "Emergency":emergency_count,
            "Nutrition and Dietetic":nutrition_and_dietetic_count,
            "Infectious Disease":infectious_disease_count
     }
     return JsonResponse(data)
 
 
#For Monthly Appointments (Line Chart) 

from django.db.models.functions import TruncMonth
from django.db.models import Count

def monthly_appointment(request):
    # Group appointments by month and count them
    monthly_appointments = (
        Appointment.objects.annotate(month=TruncMonth('appointment_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    
    # Format data for the response
    data = {
        "months": [item['month'].strftime('%B %Y') for item in monthly_appointments],
        "counts": [item['count'] for item in monthly_appointments]
    }
    
    return JsonResponse(data)


     
     
 
 
 
 
 
 
 
 
 
 
 
 
 
#For Patients Registration Trends
from django.http import JsonResponse
from django.db.models.functions import TruncMonth
from django.db.models import Count

def patient_registration_trend(request):
    # Group registrations by month
    monthly_registrations = (
        Patients.objects.annotate(month=TruncMonth('registration_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    # Format data
    data = {
        "months": [item['month'].strftime('%B %Y') for item in monthly_registrations],
        "counts": [item['count'] for item in monthly_registrations]
    }
    
    return JsonResponse(data)

  