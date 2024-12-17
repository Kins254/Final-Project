'''
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from .models import Patient, Doctor, Admin
from django.contrib import messages  # To show messages (optional)
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt

def signIn(request):
    print("Full request method:", request.method)
    print("Request headers:", request.headers)
    print("Request body:", request.body)
    if request.method == "POST":
        # Get form data
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('userType')

        # Check if any fields are empty
        if not email or not password or not user_type:
            error_message = 'All fields are required'
            return render(request, "authentication/signIn.html", {'error_message': error_message})

        # Determine the user type and fetch the user from the database
        user = None
        if user_type == "patients":
            user = Patient.objects.filter(email=email).first()
        elif user_type == "doctors":
            user = Doctor.objects.filter(email=email).first()
        elif user_type == "admin":
            user = Admin.objects.filter(email=email).first()

        # Check if the user exists and validate the password
        if user and check_password(password, user.password_hash):
            # Optionally, use Django's authentication system (if needed)
            # Authenticate the user and start a session or token
            request.session['user_id'] = user.id  # Store the user ID in the session
            return redirect('home')  # Redirect to a home page or dashboard after successful login

         # Redirect to the respective section
            if userType == "patients":
                return redirect('patients:dashboard')  # Adjust URL name as needed
            elif userType == "doctors":
                return redirect('doctors:dashboard')
            elif userType == "admin":
                return redirect('admin:dashboard')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('login')

    else:
        # If GET request, render the login page
        return render(request, "authentication/signIn.html")
'''
from django.shortcuts import render
from django.http import JsonResponse

from .models import Patient, Doctor, Admin
import json
import logging
from django.shortcuts import render
from django.http import JsonResponse
from .models import Patient, Doctor, Admin
import json
import logging
import bcrypt  # Import bcrypt instead of Django's check_password

logger = logging.getLogger(__name__)

def signIn(request):
    if request.method == "POST":
        try:
            # Log the raw request body for debugging
            logger.info(f"Raw request body: {request.body}")

            # Parse the JSON body
            data = json.loads(request.body)
            logger.info(f"Parsed data: {data}")
            email = data.get("email")
            password = data.get("password")
            user_type = data.get("userType")
            
            logger.info(f"Email: {email}")
            logger.info(f"User Type: {user_type}")

            # More detailed user lookup logging
            if user_type == "patients":
                users = Patient.objects.filter(email=email)
                logger.info(f"Patients found with this email: {users.count()}")
                user = users.first()
            elif user_type == "doctors":
                users = Doctor.objects.filter(email=email)
                logger.info(f"Doctors found with this email: {users.count()}")
                user = users.first()
            elif user_type == "admin":
                users = Admin.objects.filter(email=email)
                logger.info(f"Admins found with this email: {users.count()}")
                user = users.first()
            else:
                return JsonResponse({'error': 'Invalid user type'}, status=400)

            # Detailed password checking using bcrypt
            if user:
                logger.info(f"User found: {user}")
                logger.info(f"Stored password hash: {user.password_hash}")
                
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

                    # Return redirect URL based on user type
                    if user_type == "patients":
                        return JsonResponse({'redirect_url': '/patients/dashboard/'}, status=200)
                    elif user_type == "doctors":
                        return JsonResponse({'redirect_url': '/doctor/dashboard/'}, status=200)
                    elif user_type == "admin":
                        return JsonResponse({'redirect_url': '/administrator/dashboard/'}, status=200)
                else:
                    logger.error(f"Password verification failed for email: {email}")
                    return JsonResponse({'error': 'Invalid email or password'}, status=401)
            else:
                logger.error(f"No user found with email: {email} for type: {user_type}")
                return JsonResponse({'error': 'Invalid email or password'}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error during login: {str(e)}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
    else:
        # Render login page for GET request
        return render(request, "authentication/signIn.html")
    
    
    
    
    
    



    
'''   
# The log In section
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password  # For comparing hashed passwords
from .models import Patient, Doctor, Admin

def login(request):
    if request.method == "POST":
        userType = request.POST.get('userType')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not userType or not email or not password:
            messages.error(request, "All fields are required")
            return redirect('login')  # Redirect to the login page

        # Determine the user type and query the database
        user = None
        if userType == "patients":
            user = Patient.objects.filter(email=email).first()
        elif userType == "doctors":
            user = Doctor.objects.filter(email=email).first()
        elif userType == "admin":
            user = Admin.objects.filter(email=email).first()
        else:
            messages.error(request, "Invalid user type")
            return redirect('login')

        # Validate user credentials
        if user and check_password(password, user.password_hash):
            # Store user info in the session
            request.session['user_id'] = user.id
            request.session['user_type'] = userType

            # Redirect to the respective section
            if userType == "patients":
                return redirect('patients:dashboard')  # Adjust URL name as needed
            elif userType == "doctors":
                return redirect('doctors:dashboard')
            elif userType == "admin":
                return redirect('admin:dashboard')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('login')

    return render(request, "authentication/login.html")  # Render the login page

'''
