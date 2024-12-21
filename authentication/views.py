#For the sign In section
from Base.models import Patients
from Base.models import Doctors
from Base.models import Admin
import json
import logging
from django.shortcuts import render
from django.http import JsonResponse

import json
import logging
import bcrypt  # Import bcrypt instead of Django's check_password
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
logger = logging.getLogger(__name__)

def signIn(request):
    if request.method == "POST":
        try:
            # Log the raw request body for debugging

            # Parse the JSON body
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")
            user_type = data.get("userType")
            

            # More detailed user lookup logging
            if user_type == "patients":
                users = Patients.objects.filter(email=email)
                
                user = users.first()
            elif user_type == "doctors":
                users = Doctors.objects.filter(email=email)
                user = users.first()
            elif user_type == "admin":
                users = Admin.objects.filter(email=email)
                user = users.first()
            else:
                return JsonResponse({'error': 'Invalid user type'}, status=400)

            # Detailed password checking using bcrypt
            if user:
               
                
                # Convert stored hash and input password to bytes
                stored_hash = user.password_hash.encode('utf-8')
                input_password = password.encode('utf-8')
                
                # Log the result of password check
                is_password_correct = bcrypt.checkpw(input_password, stored_hash)
                logger.info(f"Password check result: {is_password_correct}")

                if is_password_correct:
                    # Authentication successful
                    request.session['user_id'] = user.id
                    request.session['user_type'] = user_type
                    request.session['first_name'] = user.first_name
                    #tried but still working on it
                    # Prepare detailed user response
                    user_data = {
                        'success': True,
                        'user_type': user_type,
                        'user_id': user.id,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'redirect_url': None
                    }

                    # Set redirect URL based on user type
                    if user_type == "patients":
                        user_data['redirect_url'] = '/patients/dashboard/'
                    elif user_type == "doctors":
                        user_data['redirect_url'] = '/doctors/dashboard/'
                    elif user_type == "admin":
                        user_data['redirect_url'] = '/administrator/dashboard/'

                    return JsonResponse(user_data, status=200)
                else:
                    logger.error(f"Password verification failed for email: {email}")
                    return JsonResponse({'success': False, 'error': 'Invalid email or password'}, status=401)
            else:
                logger.error(f"No user found with email: {email} for type: {user_type}")
                return JsonResponse({'success': False, 'error': 'Invalid email or password'}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error during login: {str(e)}")
            return JsonResponse({'success': False, 'error': 'Internal server error'}, status=500)
    else:
        # Render login page for GET request
        return render(request, "authentication/signIn.html")
    
    
@csrf_exempt
@require_http_methods(["POST"])
def signUp(request):
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body)
        
        # Extracting data from the request
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        address = data.get('address', '').strip()
        gender = data.get('selectedgender', '').strip()
        date_of_birth = data.get('date_of_birth', '').strip()
        password = data.get('password', '')
        
        # Validating required fields
        if not all([first_name, last_name, email, password]):
            return JsonResponse({
                'success': False, 
                'message': 'Please fill in all required fields.'
            }, status=400)

        # Checking if user already exists across all user types
        if (Patients.objects.filter(email=email).exists() ):
            return JsonResponse({
                'success': False, 
                'message': 'An account with this email already exists.'
            }, status=400)

        # Hashing the password using bcrypt
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

        try:
            # Creating a Patient by default 
            patient = Patients.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address,
                gender=gender,
                date_of_birth=date_of_birth,
                password_hash=password_hash.decode('utf-8')  # Store as string
            )
            
            logger.info(f"New patient created: {email}")
            
            return JsonResponse({
                'success': True, 
                'message': 'Registration successful!',
                'redirect_url': '/patients/dashboard/'  # Consistent with your signin logic
            }, status=201)

        except Exception as e:
            logger.error(f"Registration failed: {str(e)}")
            return JsonResponse({
                'success': False, 
                'message': f'Registration failed: {str(e)}'
            }, status=500)

    except json.JSONDecodeError:
        logger.error("Invalid JSON data received")
        return JsonResponse({
            'success': False, 
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        logger.error(f"Unexpected error during signup: {str(e)}")
        return JsonResponse({
            'success': False, 
            'message': f'An unexpected error occurred: {str(e)}'
        }, status=500)
    
    
    
    


