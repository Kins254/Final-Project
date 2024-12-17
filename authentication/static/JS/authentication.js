function toggle() {
    const div = document.getElementById("thecard"); // Assuming you have a div to rotate
    div.style.transform = "rotateY(180deg)";
  }
  
  function toggleback() {
    const div = document.getElementById("thecard"); // Assuming you have a div to rotate
    div.style.transform = "rotateY(0deg)";
  }
  
  // Validation
   // Validation
document.getElementById("myForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the form from submitting
  
    // Clear previous error messages
    document.querySelectorAll('.error').forEach(span => span.textContent = '');
  
    let isValid = true;
  
    // Validate Name
    const name = document.getElementById("name").value.trim();
    if (name === "") {
      document.getElementById("nameError").textContent = "Name is required.";
      isValid = false;
    } else {
      const nameParts = name.split(" ");
      if (nameParts.length < 2) {
        document.getElementById("nameError").textContent = "Please enter both first and last name.";
        isValid = false;
      } else {
        const first_name = nameParts[0];
        const last_name = nameParts.slice(1).join(" ");
      }
    }
  
    // Validate Email
    const email = document.getElementById("email1").value.trim();
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (email === "") {
      document.getElementById("emailError").textContent = "Email is required.";
      isValid = false;
    } else if (!emailPattern.test(email)) {
      document.getElementById("emailError").textContent = "Invalid email format.";
      isValid = false;
    }
  
    // Validate Phone
    const phone = document.getElementById("phone").value.trim();
    const phonePattern = /^\+254\d{9}$/;
    if (phone === "") {
      document.getElementById("phoneError").textContent = "Phone No is required.";
      isValid = false;
    } else if (!phonePattern.test(phone)) {
      document.getElementById("phoneError").textContent = "Invalid Phone No format.";
      isValid = false;
    }
  
    // Validate Address
    const address = document.getElementById("address").value.trim();
    if (address === "") {
      document.getElementById("addressError").textContent = "Address is required.";
      isValid = false;
    }
  
    // Validate Gender
    const selectedGender = document.querySelector('input[name="gender"]:checked');
    if (!selectedGender) {
      document.getElementById("genderError").textContent = "Gender is required.";
      isValid = false;
    }
  
    // Validate Date of Birth
    const dateOfBirth = document.getElementById("date_of_birth").value;
    if (dateOfBirth === "") {
      document.getElementById("dobError").textContent = "Date of Birth is required.";
      isValid = false;
    }
  
    // Validate Password
    const password = document.getElementById("password1").value;
    if (password === "") {
      document.getElementById("passwordError").textContent = "Password is required.";
      isValid = false;
    } else if (password.length < 8) {
      document.getElementById("passwordError").textContent = "Password must be at least 8 characters long.";
      isValid = false;
    }
  
    // Validate Confirm Password
    const confirmPassword = document.getElementById("confirm").value;
    if (confirmPassword === "") {
      document.getElementById("confirmPasswordError").textContent = "Confirm Password is required.";
      isValid = false;
    } else if (confirmPassword !== password) {
      document.getElementById("confirmPasswordError").textContent = "Passwords do not match.";
      isValid = false;
    }
  
    // Validate Terms and Conditions
    const terms = document.getElementById("terms").checked;
    if (!terms) {
      document.getElementById("termsError").textContent = "You must agree to the Terms and Conditions.";
      isValid = false;
    }
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  
    // If the form is valid, send the registration data to the server
    if (isValid) {
      const data = {
        first_name: name.split(" ")[0],
        last_name: name.split(" ").slice(1).join(" "),
        email,
        phone,
        address,
        selectedgender: selectedGender.value,
        date_of_birth: dateOfBirth,
        password
      };
      
      console.log('Sending data:', data);  // Log the data being sent
  
      fetch('http://127.0.0.1:8000/authentication/signUp/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(data),
      })
        .then(response => {
          console.log('Response status:', response.status);
          return response.json();
        })
        .then(data => {
          console.log('Response data:', data);
          if (data.success) {
            alert('Registration successful! You can now log in.');
            toggleback(); // Call the function to toggle back to the login card
          } else {
            alert(data.message || 'Registration failed. Please try again.');
          }
        })
        .catch(error => {
          console.error('Error:', error);
          alert('An error occurred. Please try again later.');
        });
    }
  });
  
  

  // JavaScript code for handling the login process
  document.getElementById('loginForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the form from submitting normally

    const userType = document.getElementById('userType').value;
    const enteredEmail = document.getElementById('email').value;
    const enteredPassword = document.getElementById('password').value;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    console.log('Attempting to login with:', { userType, enteredEmail });

    // Send a POST request to the Django server
    fetch('http://127.0.0.1:8000/authentication/signIn/', {
        method: 'POST', // Ensure the method is POST
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken, // Include CSRF token
        },
        body: JSON.stringify({
            userType,
            email: enteredEmail,
            password: enteredPassword
        }), // Send the data as JSON
    })
        .then(response => {
            console.log('Response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.redirect_url) {
                // Redirect the user to the appropriate page
                console.log('Redirecting to:', data.redirect_url);
                window.location.href = data.redirect_url;
            } else if (data.error) {
                // Display error message from server
                console.error('Server error:', data.error);
                alert(data.error);
            } else {
                console.warn('Unexpected response:', data);
                alert('Unexpected response. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again later.');
        });
});

    