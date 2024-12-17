//setting the admin_id
const userType2 = sessionStorage.getItem('userType');
console.log("Type In admin section:", userType2);

let admin_id = null; // Declare admin_id once with let

if (userType2 === "admin") {
  admin_id = sessionStorage.getItem('userId'); // Update the existing admin_id
  sessionStorage.setItem('adminId', admin_id); // Store admin_id in sessionStorage
}

console.log("The admin section admin's ID is: ", admin_id);

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
  
      // Fetch filtered data from the server
      const response = await fetch(`http://localhost:3000/Admin/patients?${queryParams.toString()}`);
      const patients = await response.json();
      console.log("Fetch response:", response); 
    
      const tbody = document.getElementById("TbodyPatAdmin");
      tbody.innerHTML = ""; // Clear existing rows
  
      patients.forEach((patient) => {
        const row = document.createElement("tr");
        row.setAttribute("data-id", patient.id); 
  
        // Populate row with patient data
        row.innerHTML = `
          <td>${patient.id}</td>
          <td>${patient.first_name}</td>
          <td>${patient.last_name}</td>
          <td>${patient.email}</td>
          <td>${patient.phone}</td>
          <td>${patient.address}</td>
          <td>${patient.gender}</td>
          <td>${patient.date_of_birth}</td>
          <td>
           
            <button class="delete-btn" onclick="deletePatient(${patient.id})">Delete</button>
          </td>
        `;
        tbody.appendChild(row);
      });
    } catch (error) {
      console.error("Error fetching patients:", error);
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

      const response = await fetch(`http://localhost:3000/adminPatient/delete/${patientId}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
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
    try {
      const id2 = document.getElementById('idFilterDoc').value;
      const email2 = document.getElementById('emailFilterDoc').value;
      const phone2 = document.getElementById('phoneFilterDoc').value;

 
  
      // Build query parameters string
      const queryParams2 = new URLSearchParams();
      if (id2) queryParams2.append('id', id2);
      if (email2) queryParams2.append('email', email2);
      if (phone2) queryParams2.append('phone', phone2);
  
      // Fetch filtered data from the server
      const response2 = await fetch(`http://localhost:3000/Admin/doctors?${queryParams2.toString()}`);
      const doctors = await response2.json();
  console.log("Response 2:",response2);
      const tbody = document.getElementById("TbodyDocAdmin");
      tbody.innerHTML = ""; // Clear existing rows
  
      doctors.forEach((doctor) => {
        const row = document.createElement("tr");
        row.setAttribute("data-id", doctor.id); 
  
        // Populate row with patient data
        row.innerHTML = `
          <td>${doctor.id}</td>
          <td>${doctor.first_name}</td>
          <td>${doctor.last_name}</td>
          <td>${doctor.email}</td>
          <td>${doctor.phone}</td>
          <td>${doctor.specialization}</td>
          <td>${doctor.schedule}</td>
          
          <td>
            
            <button class="delete-btn" onclick="deleteDoctor(${doctor.id})">Delete</button>
          </td>
        `;
        tbody.appendChild(row);
      });
    } catch (error) {
      console.error("Error fetching doctors:", error);
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

    fetch('http://localhost:3000/doc/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
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

      const response = await fetch(`http://localhost:3000/adminDoctor/delete/${doctorId}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
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
        try {
          const id3 = document.getElementById('idFilterApp').value;
          const patientID = document.getElementById('patientIdFilterApp').value;
          const doctorID = document.getElementById('doctorIdFilterApp').value;
    
         
      
          // Build query parameters string
          const queryParams3 = new URLSearchParams();
          if (id3) queryParams3.append('id', id3);
          if (patientID) queryParams3.append('patient_id', patientID);
          if (doctorID) queryParams3.append('doctor_id', doctorID);
      
          // Fetch filtered data from the server
          const response = await fetch(`http://localhost:3000/Admin/appointments?${queryParams3.toString()}`);
          const appointments = await response.json();
      
          const tbody = document.getElementById("TbodyAppAdmin");
          tbody.innerHTML = ""; // Clear existing rows
      
          appointments.forEach((appointment) => {
            const row = document.createElement("tr");
            row.setAttribute("data-id", appointment.id); 
      
            // Populate row with patient data
            row.innerHTML = `
              <td>${appointment.id}</td>
              <td>${appointment.patient_id}</td>
              <td>${appointment.doctor_id}</td>
              <td>${appointment.appointment_date}</td>
              <td>${appointment.appointment_time}</td>
              <td>${appointment.appointment_type}</td>
              <td>${appointment.communication_type}</td>
              <td>${appointment.payment_type}</td>
              
              <td>
                <button class="edit-btn" onclick="editRow(${appointment.id})">Edit</button>
                <button class="delete-btn" onclick="deleteAppointment(${appointment.id})">Delete</button>
              </td>
            `;
            tbody.appendChild(row);
          });
        } catch (error) {
          console.error("Error fetching appointments:", error);
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