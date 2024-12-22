import json
import bcrypt
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
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
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


#For Updating appointments
@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def updating_appointment(request, appointment_id):
    
    try:
        # Parse JSON data from request body
        data = json.loads(request.body)
        
        # Retrieve the appointment
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            logger.warning(f"Appointment {appointment_id} not found")
            return JsonResponse({
                'success': False,
                'error': 'Appointment not found'
            }, status=404)

        # Update appointment fields if provided in the request
        if 'appointment_type' in data:
            appointment.appointment_type = data['appointment_type']
        if 'doctor_id' in data:
            appointment.doctor_id = data['doctor_id']
        if 'appointment_date' in data:
            appointment.appointment_date = data['appointment_date']
        if 'appointment_time' in data:
            appointment.appointment_time = data['appointment_time']
        if 'communication_type' in data:
            appointment.communication_type = data['communication_type']
        if 'payment_type' in data:
            appointment.payment_type = data['payment_type']

        # Save the updated appointment
        try:
            with transaction.atomic():
                appointment.save()
                logger.info(f"Appointment {appointment_id} updated successfully")
                return JsonResponse({
                    'success': True,
                    'message': 'Appointment updated successfully',
                    'appointment_id': appointment_id
                })
        except Exception as e:
            logger.error(f"Error saving updated appointment: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': 'Failed to save appointment updates'
            }, status=500)

    except json.JSONDecodeError:
        logger.error("Invalid JSON in request body")
        return JsonResponse({
            'success': False,
            'error': 'Invalid request format'
        }, status=400)
    except Exception as e:
        logger.error(f"Unexpected error updating appointment: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'An unexpected error occurred'
        }, status=500)




#Appointment deleting section 
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_appointment(request):
    logger.info("Delete appointment request received")
    
    try:
        # Parse JSON data from request body
        data = json.loads(request.body)
        appointment_id = data.get('id')
        
        if not appointment_id:
            logger.warning("No appointment ID provided in delete request")
            return JsonResponse({
                'success': False,
                'error': 'Appointment ID is required'
            }, status=400)
            
        try:
            # Get the appointment
            appointment = Appointment.objects.get(id=appointment_id)
            
            # Delete the appointment
            with transaction.atomic():
                appointment.delete()
                logger.info(f"Appointment {appointment_id} deleted successfully")
                
                return JsonResponse({
                    'success': True,
                    'message': 'Appointment deleted successfully'
                })
                
        except Appointment.DoesNotExist:
            logger.warning(f"Appointment {appointment_id} not found for deletion")
            return JsonResponse({
                'success': False,
                'error': 'Appointment not found'
            }, status=404)
            
        except Exception as e:
            logger.error(f"Error deleting appointment: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': 'Failed to delete appointment'
            }, status=500)
            
    except json.JSONDecodeError:
        logger.error("Invalid JSON in delete request body")
        return JsonResponse({
            'success': False,
            'error': 'Invalid request format'
        }, status=400)
        
    except Exception as e:
        logger.error(f"Unexpected error in delete appointment: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'An unexpected error occurred'
        }, status=500)


#For updating the account


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

        # Retrieve the user by userId and email
        try:
            user = Patients.objects.get(id=userId)
        except Patients.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'No user found with this email and userId'
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

from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_protect

logger = logging.getLogger(__name__)
@csrf_protect
@require_http_methods(["DELETE"])
def delete_account(request):
   
        

    try:
        # Get and verify session
        session_user_id = request.session.get('user_id')
        if not session_user_id:
            return JsonResponse({
                'success': False,
                'message': 'No active session found'
            }, status=401)

        # Parse request body
        data = json.loads(request.body)
        patient_id = data.get('patient_id')
        
        if not patient_id:
            return JsonResponse({
                'success': False,
                'message': 'Patient ID not provided'
            }, status=400)
        
        # Verify the patient_id matches the logged-in user's ID
        if str(patient_id) != str(session_user_id):
            return JsonResponse({
                'success': False,
                'message': 'Unauthorized deletion attempt'
            }, status=403)
        print(Patients.objects.all())
        
        # Delete the user
        user = Patients.objects.get(id=patient_id)
        user.delete()
        print(Patients.objects.all())
        
        # Clear session
        request.session.flush()
        
        return JsonResponse({
            'success': True,
            'message': 'Account deleted successfully'
        })
        
    except Patients.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'User not found'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        print(f"Error in delete_account: {str(e)}")  # Add logging
        return JsonResponse({
            'success': False,
            'message': f'Error deleting account: {str(e)}'
        }, status=500)