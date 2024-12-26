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


#For the Appointment section
from django.db.models import Q
from datetime import datetime
from django.core.exceptions import ValidationError
@csrf_exempt
@require_http_methods(["GET"])
def view_appointment(request):
    try:
        appointment_id = request.GET.get("id")  # Use GET parameters
        patient_id = request.GET.get("patientId")
        appointment_date = request.GET.get("date")
        doctor_id = request.GET.get("doctorId")  # Ensure it's passed correctly

        # Base query
        appointment = Appointment.objects.filter(doctor_id=doctor_id)

        # Filter based on parameters
        if appointment_id:
            appointment = appointment.filter(id=appointment_id)

        if patient_id:
            appointment = appointment.filter(patient_id=patient_id)

        if appointment_date:
            appointment = appointment.filter(appointment_date=appointment_date)

        # Convert queryset to a list of dictionaries
        appointment_data = list(appointment.values(
            'id',
            'patient_id',
            'appointment_date',
            'appointment_time',
            'appointment_type',
            'communication_type',
            'payment_type',
            'status'
        ))

        return JsonResponse(appointment_data, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)




#For Approving an appointment
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
#@login_required
@csrf_exempt
@require_http_methods(["PUT"])
def approve_appointment(request, appointment_id):
    """
    Approve a specific appointment
    """
    try:
        # Retrieve the appointment
        appointment = get_object_or_404(Appointment, id=appointment_id)

        # Update status
        appointment.status = 'Approved'
        appointment.save()

        # Return the updated status
        return JsonResponse({
            'message': 'Appointment approved successfully',
            'id': appointment_id,
            'status': appointment.status
        })

    except Appointment.DoesNotExist:
        return JsonResponse({'error': 'Appointment not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

#For completing an Appointment
@csrf_exempt
@require_http_methods(["PUT"])
def complete_appointment(request, appointment_id):
  
    try:
        # Retrieve the appointment
        appointment = get_object_or_404(Appointment, id=appointment_id)

        # Update status
        appointment.status = 'Completed'
        appointment.save()

        # Return the updated status
        return JsonResponse({
            'message': 'Appointment Completedd successfully',
            'id': appointment_id,
            'status': appointment.status
        })

    except Appointment.DoesNotExist:
        return JsonResponse({'error': 'Appointment not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)




#For deleteing an appointment


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_appointment(request, appointment_id):
  
    try:
        # Retrieve the appointment
        appointment = get_object_or_404(Appointment, id=appointment_id)

        with transaction.atomic():
                appointment.delete()
                logger.info(f"Appointment {appointment_id} deleted successfully")
                
                return JsonResponse({
                    'success': True,
                    'message': 'Appointment deleted successfully'
                })

    except Appointment.DoesNotExist:
        return JsonResponse({'error': 'Appointment not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)







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




#Account Deleting section

logger = logging.getLogger(__name__)
@csrf_protect
@require_http_methods(["DELETE"])
def delete_account(request):
    try:
        # Log the incoming request
        logger.debug(f"Delete account request received with body: {request.body}")
        
        # Get and verify session
        session_user_id = request.session.get('user_id')
        logger.debug(f"Session user_id: {session_user_id}")
        
        if not session_user_id:
            logger.warning("No active session found")
            return JsonResponse({
                'success': False,
                'message': 'No active session found'
            }, status=401)

        # Parse request body
        data = json.loads(request.body)
        doctor_id = data.get('doctor_id')
        logger.debug(f"Received doctor_id: {doctor_id}")
        
        if not doctor_id:
            logger.warning("Doctor ID not provided in request")
            return JsonResponse({
                'success': False,
                'message': 'Doctor ID not provided'
            }, status=400)
        
        # Verify the doctor_id matches the logged-in user's ID
        if str(doctor_id) != str(session_user_id):
            logger.warning(f"Session ID ({session_user_id}) does not match requested doctor_id ({doctor_id})")
            return JsonResponse({
                'success': False,
                'message': 'Unauthorized deletion attempt'
            }, status=403)

        try:
            user = Doctors.objects.get(id=doctor_id)
            logger.info(f"Found doctor to delete: {user.email}")
            user.delete()
            logger.info(f"Successfully deleted doctor with ID: {doctor_id}")
            
            # Clear session
            request.session.flush()
            logger.info("Session cleared")
            
            return JsonResponse({
                'success': True,
                'message': 'Account deleted successfully'
            })
            
        except Doctors.DoesNotExist:
            logger.error(f"Doctor with ID {doctor_id} not found in database")
            return JsonResponse({
                'success': False,
                'message': 'User not found'
            }, status=404)
            
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        logger.error(f"Unexpected error in delete_account: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': f'Error deleting account: {str(e)}'
        }, status=500)