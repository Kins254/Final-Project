import json
import logging
from Base.models import Doctors
from Base.models import Patients
from Base.models import Appointment
from django.db import transaction
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


def patients(request):
   return render(request, 'patients/patients.html')



#For Log In
from django.shortcuts import render,redirect

def dashboard(request):
    user_id = request.session.get('user_id')  # Retrieve the user ID from the session
    if not user_id:
        return redirect('authentication:login')  # Redirect to login if no user ID in session

    # Fetch additional patient details if needed
    return render(request, "patients/patients.html", {"user_id": user_id})



def book_appointments(request):
   return render(request, 'patients/patients.html')

#Bookin an appointment section


logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST"])
def book_appointment(request):
    try:
        # Parse JSON data from request body
        data = json.loads(request.body)
        
        # Extract data from POST request
        patient_id = data.get('patient_id')
        doctor_id = data.get('doctor_id')
        appointment_type = data.get('appointment_type')
        appointment_date = data.get('appointment_date')
        appointment_time = data.get('appointment_time')
        communication_type = data.get('communication_type')
        payment_type = data.get('payment_type')

     
        # Validate required fields
        if not all([patient_id, doctor_id, appointment_type, 
                    appointment_date, appointment_time, 
                    communication_type, payment_type]):
            logger.warning("Missing required appointment details")
            return JsonResponse({
                'success': False, 
                'error': 'Missing required appointment details'
            }, status=400)

        # Create appointment
        try:
            with transaction.atomic():
                appointment = Appointment.objects.create(
                    patient_id=patient_id,
                    doctor_id=doctor_id,
                    appointment_type=appointment_type,
                    appointment_date=appointment_date,
                    appointment_time=appointment_time,
                    communication_type=communication_type,
                    payment_type=payment_type,
                    status='Pending'
                )

            # Confirm database persistence
            created_appointment = Appointment.objects.filter(id=appointment.id).exists()
            if created_appointment:
                return JsonResponse({
                    'success': True, 
                    'appointment_id': appointment.id,
                    'message': 'Appointment booked successfully and saved in the database'
                }, status=201)
            else:
                logger.error("Appointment was created but not found in the database")
                return JsonResponse({
                    'success': False,
                    'error': 'Appointment creation failed to persist'
                }, status=500)
        except Exception as e:
            logger.error(f"Appointment creation error: {str(e)}")
            return JsonResponse({
                'success': False, 
                'error': 'Failed to create appointment'
            }, status=500)
    except json.JSONDecodeError:
        logger.error("Invalid JSON in request body")
        return JsonResponse({
            'success': False, 
            'error': 'Invalid request format'
        }, status=400)
    except Exception as e:
        logger.error(f"Unexpected error in booking appointment: {str(e)}")
        return JsonResponse({
            'success': False, 
            'error': 'Unexpected error occurred'
        }, status=500)



#Viewing An appointment section
# patients/views.py

'''
def view_appointment(request, patient_id):
    try:
        # Fetch appointments for the patient
        appointments = Appointment.objects.filter(patient_id=patient_id)
        
        # Serialize the appointment data (you can add fields as needed)
        appointment_data = []
        for appointment in appointments:
            appointment_data.append({
                "id": appointment.id,
                "doctor_id": appointment.doctor_id,
                "appointment_date": appointment.appointment_date.strftime('%Y-%m-%d'),
                "appointment_time": appointment.appointment_time.strftime('%H:%M:%S'),
                "appointment_type": appointment.appointment_type,
                "communication_type": appointment.communication_type,
                "payment_type": appointment.payment_type
            })
        
        return JsonResponse(appointment_data, safe=False)  # safe=False to return a list
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

'''

