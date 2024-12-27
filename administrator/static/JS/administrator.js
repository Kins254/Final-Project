//setting the admin_id
const sessionData = document.getElementById('session-data');
const userType = sessionData.dataset.userType;
let admin_id = null;
let first_name = null;

if(userType==="admin"){
  admin_id = sessionData.dataset.adminId;
   first_name = sessionData.dataset.firstName;


}
else{
  admin_id = null;
   first_name = null;
}

console.log("Type In patient section:", userType);
console.log("Admin Id:", admin_id);
console.log("Admin's First name:", first_name);

/*
///Header greetings
 // Function to get the current greeting based on time
 function getGreeting() {
  const currentHour = new Date().getHours();
  let greeting;

  if (currentHour >= 5 && currentHour < 12) {
      greeting = "Good morning";
  } else if (currentHour >= 12 && currentHour < 18) {
      greeting = "Good afternoon";
  } else {
      greeting = "Good evening";
  }

  return greeting;
}

const greetingsElement=document.getElementById('greetingsPat');
greetingsElement.textContent= `${getGreeting()}`

const usernames=document.getElementById('usernamePat');
const username1= first_name;

if (username1) {
  usernames.textContent = ` ${username1}!`;
} else {
  usernames.textContent = `Guest!`; // Fallback if no name is stored
}

*/


//fetching the patients data
async function AdminPatientsFetch() {
  console.log("AdminPatientsFetch function triggered");
  console.log("Fetching data...");
  
  try {
    const id = document.getElementById('idFilterPat').value;
    const email = document.getElementById('emailFilterPat').value;
    const phone = document.getElementById('phoneFilterPat').value;
    
    // Build query parameters string
    const queryParams = new URLSearchParams();
    if (id) queryParams.append('id', id);
    if (email) queryParams.append('email', email);
    if (phone) queryParams.append('phone', phone);

    const url = `http://127.0.0.1:8000/administrator/fetch_patients?${queryParams.toString()}`;
    console.log("Fetching from URL:", url);

    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const responseData = await response.json();
    console.log("Received patients data:", responseData);

    // Extract the patients array from the data property
    const patients = responseData.data;

    const tbody = document.getElementById("TbodyPatAdmin");
    if (!tbody) {
      throw new Error("Table body element not found!");
    }
    
    tbody.innerHTML = ""; // Clear existing rows

    // Handle case where no patients are found
    if (!patients || patients.length === 0) {
      const row = document.createElement("tr");
      row.innerHTML = '<td colspan="9" class="text-center">No patients found</td>';
      tbody.appendChild(row);
      return;
    }

    patients.forEach((patient) => {
      const row = document.createElement("tr");
      row.setAttribute("data-id", patient.id);

      // Safely handle potentially null or undefined values
      const safeText = (text) => text || '';
      
      row.innerHTML = `
        <td>${safeText(patient.id)}</td>
        <td>${safeText(patient.first_name)}</td>
        <td>${safeText(patient.last_name)}</td>
        <td>${safeText(patient.email)}</td>
        <td>${safeText(patient.phone)}</td>
        <td>${safeText(patient.address)}</td>
        <td>${safeText(patient.gender)}</td>
        <td>${safeText(patient.date_of_birth)}</td>
        <td>
          <button class="delete-btn" onclick="deletePatient(${patient.id})">Delete</button>
        </td>
      `;
      tbody.appendChild(row);
    });
  } catch (error) {
    console.error("Error fetching patients:", error);
    
    // Display error message to user
    const tbody = document.getElementById("TbodyPatAdmin");
    if (tbody) {
      tbody.innerHTML = `
        <tr>
          <td colspan="9" class="text-center text-red-500">
            Error loading patients: ${error.message}
          </td>
        </tr>
      `;
    }
  }
}

// Call the fetch function when the page loads
window.onload = AdminPatientsFetch;
  


//Api For deleting the patient

async function deletePatient(patientId) {
  const userConfirm = confirm("Do you want to delete this Patient?");
  if (userConfirm) {
    try {
      // Check if patientId is valid before making the request
      if (!patientId || isNaN(patientId)) {
        alert("Invalid Patient ID.");
        return;
      }
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      const response = await fetch(`http://127.0.0.1:8000/administrator/delete_patient/${patientId}/`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json,',
          'X-CSRFToken': csrfToken 

        },
      });

      if (!response.ok) {
        throw new Error('Failed to delete Patient status.');
      }

      

      alert(`Patient ${patientId} has been deleted.`);
    } catch (error) {
      console.error('Error deleting patient:', error);
      alert("Failed to deleting Patient.");
    }
  } else {
    alert("Action canceled.");
  }
}


  //fetching the doctor's section

  async function AdminDoctorsFetch() {
    console.log("AdminDoctorsFetch function triggered");
    console.log("Fetching doctors data...");
    
    try {
      const id = document.getElementById('idFilterDoc').value;
      const email = document.getElementById('emailFilterDoc').value;
      const phone = document.getElementById('phoneFilterDoc').value;
      
      // Build query parameters string
      const queryParams = new URLSearchParams();
      if (id) queryParams.append('id', id);
      if (email) queryParams.append('email', email);
      if (phone) queryParams.append('phone', phone);
  
      const url = `http://127.0.0.1:8000/administrator/fetch_doctors?${queryParams.toString()}`;
      console.log("Fetching from URL:", url);
  
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const responseData = await response.json();
      console.log("Received doctors data:", responseData);
  
      // Extract the doctors array from the data property
      const doctors = responseData.data;
  
      const tbody = document.getElementById("TbodyDocAdmin");
      if (!tbody) {
        throw new Error("Table body element not found!");
      }
      
      tbody.innerHTML = ""; // Clear existing rows
  
      // Handle case where no doctors are found
      if (!doctors || doctors.length === 0) {
        const row = document.createElement("tr");
        row.innerHTML = '<td colspan="8" class="text-center">No doctors found</td>';
        tbody.appendChild(row);
        return;
      }
  
      doctors.forEach((doctor) => {
        const row = document.createElement("tr");
        row.setAttribute("data-id", doctor.id);
  
        // Safely handle potentially null or undefined values
        const safeText = (text) => text || '';
        
        row.innerHTML = `
          <td>${safeText(doctor.id)}</td>
          <td>${safeText(doctor.first_name)}</td>
          <td>${safeText(doctor.last_name)}</td>
          <td>${safeText(doctor.email)}</td>
          <td>${safeText(doctor.phone)}</td>
          <td>${safeText(doctor.specialization)}</td>
          <td>${safeText(doctor.schedule)}</td>
          <td>
            <button class="delete-btn" onclick="deleteDoctor(${doctor.id})">Delete</button>
          </td>
        `;
        tbody.appendChild(row);
      });
    } catch (error) {
      console.error("Error fetching doctors:", error);
      
      // Display error message to user
      const tbody = document.getElementById("TbodyDocAdmin");
      if (tbody) {
        tbody.innerHTML = `
          <tr>
            <td colspan="8" class="text-center text-red-500">
              Error loading doctors: ${error.message}
            </td>
          </tr>
        `;
      }
    }
  }
  
  // Call the fetch function when the page loads
  window.onload = AdminDoctorsFetch;




//Adding doctors section

// Validation
document.querySelector(".DocAdding").addEventListener("submit", function (event) {
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
  const email = document.getElementById("email").value.trim();
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

 //schedule
 const schedule=document.getElementById("schedule2").value;

 //for specialization
 const specialization=document.getElementById("specialization").value;

 

  // Validate Password
  const password = document.getElementById("passwordDoc").value;
  if (password === "") {
    document.getElementById("passwordError").textContent = "Password is required.";
    isValid = false;
  } else if (password.length < 8) {
    document.getElementById("passwordError").textContent = "Password must be at least 8 characters long.";
    isValid = false;
  }

  // Validate Confirm Password
  const confirmPassword = document.getElementById("confirmDocAcc").value;
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

  // If the form is valid, send the registration data to the server
  if (isValid) {
    const data = {
      first_name: name.split(" ")[0],
      last_name: name.split(" ").slice(1).join(" "),
      email,
      phone,
     specialization,
     schedule,
      password
    };
    
    console.log('Sending data:', data);  // Log the data being sent
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('http://127.0.0.1:8000/administrator/doctor_account/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify(data),
    })
      .then(response => {
        console.log('Doctor Regestration Data:', response.status);
        return response.json();
      })
      .then(data => {
        console.log('Response data:', data);
        if (data.success) {
          alert('Registration successful! ');
            // Optionally clear the form:
          document.querySelector(".DocAdding").reset();
          
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


///API for deleting Doctors
async function deleteDoctor(doctorId) {
  const userConfirm = confirm("Do you want to delete this Doctor?");
  if (userConfirm) {
    try {
      // Check if doctorId is valid before making the request
      if (!doctorId || isNaN(doctorId)) {
        alert("Invalid Doctor ID.");
        return;
      }
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

      const response = await fetch(`http://127.0.0.1:8000/administrator/delete_doctor/${doctorId}/`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken  },
      });

      if (!response.ok) {
        throw new Error('Failed to delete Doctor status.');
      }

      

      alert(`Doctor  ${doctorId} has been deleted.`);
    } catch (error) {
      console.error('Error deleting Doctor:', error);
      alert("Failed to deleting Doctor.");
    }
  } else {
    alert("Action canceled.");
  }
}






    //fetching the appointment's section

    async function AdminAppointmentFetch() {
      console.log("AdminAppointmentFetch function triggered");
      console.log("Fetching appointments data...");
    
      try {
        const id = document.getElementById('idFilterApp').value;
        const patientId = document.getElementById('patientIdFilterApp').value;
        const doctorId = document.getElementById('doctorIdFilterApp').value;
        
        // Build query parameters string
        const queryParams = new URLSearchParams();
        if (id) queryParams.append('id', id);
        if (patientId) queryParams.append('patient_id', patientId);
        if (doctorId) queryParams.append('doctor_id', doctorId);
    
        const url = `http://127.0.0.1:8000/administrator/view_appointments?${queryParams.toString()}`;
        console.log("Fetching from URL:", url);
    
        const response = await fetch(url);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const responseData = await response.json();
        console.log("Received appointments data:", responseData);
    
        // Extract the appointments array from the data property
        const appointments = responseData.data;
    
        const tbody = document.getElementById("TbodyAppAdmin");
        if (!tbody) {
          throw new Error("Table body element not found!");
        }
        
        tbody.innerHTML = ""; // Clear existing rows
    
        // Handle case where no appointments are found
        if (!appointments || appointments.length === 0) {
          const row = document.createElement("tr");
          row.innerHTML = '<td colspan="9" class="text-center">No appointments found</td>';
          tbody.appendChild(row);
          return;
        }
    
        appointments.forEach((appointment) => {
          const row = document.createElement("tr");
          row.setAttribute("data-id", appointment.id);
    
          // Safely handle potentially null or undefined values
          const safeText = (text) => text || '';
          
          row.innerHTML = `
            <td>${safeText(appointment.id)}</td>
            <td>${safeText(appointment.patient_id)}</td>
            <td>${safeText(appointment.doctor_id)}</td>
            <td>${safeText(appointment.appointment_date)}</td>
            <td>${safeText(appointment.appointment_time)}</td>
            <td>${safeText(appointment.appointment_type)}</td>
            <td>${safeText(appointment.communication_type)}</td>
            <td>${safeText(appointment.payment_type)}</td>
            <td>
              <button class="edit-btn" onclick="editRow(${appointment.id})">Edit</button>
              <button class="delete-btn" onclick="deleteAppointment(${appointment.id})">Delete</button>
            </td>
          `;
          tbody.appendChild(row);
        });
      } catch (error) {
        console.error("Error fetching appointments:", error);
        
        // Display error message to user
        const tbody = document.getElementById("TbodyAppAdmin");
        if (tbody) {
          tbody.innerHTML = `
            <tr>
              <td colspan="9" class="text-center text-red-500">
                Error loading appointments: ${error.message}
              </td>
            </tr>
          `;
        }
      }
    }
    
    // Call the fetch function when the page loads
    window.onload = AdminAppointmentFetch;



///Account Update
document.getElementById("updateAccountFormAdmin").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the form from submitting
  
    // Clear previous error messages
    document.querySelectorAll('.errorEditAdmin').forEach(span => span.textContent = '');
  
    let isValid = true;
  
    // Validate Email
    const newEmail = document.getElementById("newEmailAdmin").value.trim();
    const newEmailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (newEmail === "") {
      document.getElementById("emailEditAdmin").textContent = "Email is required.";
      isValid = false;
    } else if (!newEmailPattern.test(newEmail)) {
      document.getElementById("emailEditAdmin").textContent = "Invalid email format.";
      isValid = false;
    }


    // validate current password
    const ConfirmPassword=document.getElementById("currentPasswordAdmin").value;
    if(ConfirmPassword===""){
        document.getElementById("currentPasswordEditAdmin").textContent="Password is required."
    }else if (ConfirmPassword.length < 8) {
        document.getElementById("currentPasswordEditAdmin").textContent = "Password must be at least 8 characters long.";
        isValid = false;
      }
      

    // Validate New Password
    const newPassword = document.getElementById("newPasswordAdmin").value;
    if (newPassword === "") {
      document.getElementById("newPasswordEditAdmin").textContent = "Password is required.";
      isValid = false;
    } else if (newPassword.length < 8) {
      document.getElementById("newPasswordEditAdmin").textContent = "Password must be at least 8 characters long.";
      isValid = false;
    }
  
    // Validate Confirm Password
    const confirmPassword = document.getElementById("confirmPasswordAdmin").value;
    if (confirmPassword === "") {
      document.getElementById("confirmPasswordErrorAdmin").textContent = "Confirm Password is required.";
      isValid = false;
    } else if (confirmPassword !== newPassword) {
      document.getElementById("confirmPasswordErrorAdmin").textContent = "Passwords do not match.";
      isValid = false;
    }
    
    
    if (isValid) {
        const data3 = {
            email: newEmail,
            password:ConfirmPassword,
            newpassword: newPassword,
            userId:admin_id
        };
        console.log('Sending data:', data3);
        
        fetch('http://localhost:3000/AccountEditAdmin', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data3),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response is not OK');
            } else {
                return response.json();
            }
        })
        .then(data3 => {
            if (data3.success) {
                alert("Credentials updated successfully");
            } else {
                alert("Credentials update failed");
            }
        })
        .catch(error => {
            console.error("Updating error:", error);
        });
    }
});



//Logout API
 
//first trial
document.getElementById('logout').addEventListener('click', function() {
  // Remove user session from localStorage
  sessionStorage.removeItem('userSession'); 

  // If you're using cookies to store session info, clear the cookie
  document.cookie = 'userSession=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;'; // Clear the cookie

  // Redirect to login page or home page
  window.location.href = 'http://127.0.0.1:8000/authentication/signIn/'; // or your homepage URL
});




// toggle sections

// Function to toggle the sliding panels
function toggleSlide(contentId) { 
  // First, close any open panels and disable settings
  const allPanels = document.querySelectorAll('.slidingContent');
  allPanels.forEach(panel => {
    panel.classList.remove('active');
  });

  // Then, toggle the clicked panel
  const content = document.getElementById(contentId);
  content.classList.toggle('active');

  // Close settings if it's open
  const settingsContent = document.querySelector('.settingsContent');
  settingsContent.classList.remove('active');
}




// Function to toggle the settings content
function toggleSettings() {
  // Close any open panels
  const allPanels = document.querySelectorAll('.slidingContent');
  allPanels.forEach(panel => {
    panel.classList.remove('active');
  });

  // Toggle the settings content
  const content2 = document.querySelector('.settingsContent');
  content2.classList.toggle('active');
}


//for account updates
 
 function ModalAdmin() {
  // Select the modal and parent div
  var popup = document.querySelector('.modalAdmin');
  var parent = document.querySelector('.settingsContent');

  // Toggle the active class on the modal
  popup.classList.toggle('active');

  // If the modal is active, add the blur effect to the parent and change its class to .blur
  if (popup.classList.contains('active')) {
    parent.classList.add('blur');  // Add blur effect
    parent.classList.remove('active'); // Remove the active class, if necessary
  } else {
    parent.classList.remove('blur'); // Remove blur effect
    parent.classList.add('active');  // Add back active class, if necessary
  }
}


//For adding doctors
function ModalAddDoc() {
  // Select the modal and parent div
  var popup = document.querySelector('.AddingDoctor');
  var parent = document.querySelector('#doctorContent');

  // Toggle the active class on the modal
  popup.classList.toggle('active');

  // If the modal is active, add the blur effect to the parent and change its class to .blur
  if (popup.classList.contains('active')) {
    parent.classList.add('blur');  // Add blur effect
    parent.classList.remove('active'); // Remove the active class, if necessary
  } else {
    parent.classList.remove('blur'); // Remove blur effect
    parent.classList.add('active');  // Add back active class, if necessary
  }
}