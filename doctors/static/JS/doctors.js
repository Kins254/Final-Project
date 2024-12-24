//setting the doctor_id
const sessionData = document.getElementById('session-data');
const userType = sessionData.dataset.userType;
let doctor_id = null;
let first_name = null;

if(userType==="doctors"){
   doctor_id = sessionData.dataset.doctorId;
   first_name = sessionData.dataset.firstName;


}
else{
  doctor_id = null;
   first_name = null;
}

console.log("User Type:", userType);
console.log("Doctor's Id:", doctor_id);
console.log("Doctor's First name:", first_name);


// Function to edit account details
document.getElementById("updateAccountFormDoc").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the form from submitting
  
    // Clear previous error messages
    document.querySelectorAll('.errorEditDoc').forEach(span => span.textContent = '');
  
    let isValid = true;
  
    // Validate Email
    const newEmail = document.getElementById("newEmailDoc").value.trim();
    const newEmailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (newEmail === "") {
      document.getElementById("emailEditDoc").textContent = "Email is required.";
      isValid = false;
    } else if (!newEmailPattern.test(newEmail)) {
      document.getElementById("emailEditDoc").textContent = "Invalid email format.";
      isValid = false;
    }


    // validate current password
    const ConfirmPassword=document.getElementById("currentPasswordDoc").value;
    if(ConfirmPassword===""){
        document.getElementById("currentPasswordEditDoc").textContent="Password is required."
    }else if (ConfirmPassword.length < 8) {
        document.getElementById("currentPasswordEditDoc").textContent = "Password must be at least 8 characters long.";
        isValid = false;
      }
      

    // Validate New Password
    const newPassword = document.getElementById("newPasswordDoc").value;
    if (newPassword === "") {
      document.getElementById("newPasswordEditDoc").textContent = "Password is required.";
      isValid = false;
    } else if (newPassword.length < 8) {
      document.getElementById("newPasswordEditDoc").textContent = "Password must be at least 8 characters long.";
      isValid = false;
    }
  
    // Validate Confirm Password
    const confirmPassword = document.getElementById("confirmPasswordDoc").value;
    if (confirmPassword === "") {
      document.getElementById("confirmPasswordErrorDoc").textContent = "Confirm Password is required.";
      isValid = false;
    } else if (confirmPassword !== newPassword) {
      document.getElementById("confirmPasswordErrorDoc").textContent = "Passwords do not match.";
      isValid = false;
    }
    
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    if (isValid) {
        const data3 = {
            email: newEmail,
            password:ConfirmPassword,
            newpassword: newPassword,
            userId :doctor_id
        };
       
        fetch("http://127.0.0.1:8000/doctors/account_edit/", {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': csrfToken,
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


//appointment section
//Appointment Display API
/* Function to fetch appointments and populate the table()
async function fetchDocAppointments() {
  try {
   // Retrieve user ID from local storage
  
   const doctor_id = sessionStorage.getItem('userId');
    console.log("DoctorControll ID:",doctor_id);
    const response = await fetch(`http://localhost:8000/doctors/appointments/${doctor_id}/`);
    const appointments = await response.json();

    const tbody = document.getElementById("");
    tbody.innerHTML = "";

    appointments.forEach((appointment) => {
      const row = document.createElement("tr");
      row.setAttribute("data-id", appointment.id); // Set the row's data-id attribute for easy retrieval later

      // Populate row with appointment data
      row.innerHTML = `
                <td>${appointment.id}</td>
                <td>${appointment.patient_id}</td>
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

// Call the fetchAppointments function when the page loads
window.onload = fetchDocAppointments;
*/
// Appointment section updated


async function DocAppointmentFetch() { 
  try { 
    if (!doctor_id) { 
      console.error("Doctor ID is not set. Make sure you're logged in as a doctor."); 
      return; 
    } 
 
    const Appid3 = document.getElementById('idFilterAppDoc').value; 
    const PatId3 = document.getElementById('patientIdFilterAppDoc').value; 
    const date3 = document.getElementById('AppointmentDateFilterAppDoc').value; 
 
    console.log("Doctor ID in use(Appointment):", doctor_id); 
 
    const queryParams3 = new URLSearchParams(); 
    queryParams3.append('doctorId', doctor_id);
    if (Appid3) queryParams3.append('id', Appid3); 
    if (PatId3) queryParams3.append('patientId', PatId3); 
    if (date3) queryParams3.append('date', date3); 
 
    const response3 = await fetch(`http://127.0.0.1:8000/doctors/view_appointment?${queryParams3.toString()}`); 
    const appointments = await response3.json(); 
 
    console.log("Fetched Appointments:", appointments); 
 
    const tbody = document.getElementById("TbodyAppDoc"); 
    tbody.innerHTML = ""; // Clear existing rows 
 
    // Remove the additional filtering, as it's already handled server-side
    appointments.forEach((appointment) => { 
      const row = document.createElement("tr"); 
      row.setAttribute("data-id", appointment.id); 
 
      row.innerHTML = ` 
        <td>${appointment.id}</td> 
        <td>${appointment.patient_id}</td> 
        
        <td>${appointment.appointment_date}</td> 
        <td>${appointment.appointment_time}</td> 
        <td>${appointment.appointment_type}</td> 
        <td>${appointment.communication_type}</td> 
        <td>${appointment.payment_type}</td> 
        <td>${appointment.status} </td> 
        <td> 
          <button class="edit-btnAppDoc" onclick="ApproveRow(${appointment.id})">Approve</button> 
                    <button class="completed-btnAppDoc" onclick="CompletedRow(${appointment.id})">Completed</button> 

          <button class="delete-btnAppDoc" onclick="deleteAppointment(${appointment.id})">Delete</button> 
        </td> 
      `; 
      tbody.appendChild(row); 
    }); 
  } catch (error) { 
    console.error("Error fetching appointments:", error); 
  } 
}


// Call the fetch function when the page loads
document.addEventListener("DOMContentLoaded", () => {
  console.log("Page loaded. Calling DocAppointmentFetch.");
  DocAppointmentFetch();
});


//appointment approval
async function ApproveRow(appointmentId) {
  const userConfirm = confirm("Do you want to approve this appointment?");
  if (userConfirm) {
    try {
      // Validate the appointmentId
      if (!appointmentId || isNaN(appointmentId)) {
        alert("Invalid appointment ID.");
        return;
      }
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      const url = `http://127.0.0.1:8000/doctors/approve_appointment/${appointmentId}/`;
      console.log('Making request to:', url);
      console.log('Method:', 'PUT');
      // Send the PUT request
      const response = await fetch(url, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': csrfToken,
         },
      });
      console.log('Attempting to fetch:', url);
      console.log('Response status:', response.status);
      console.log('Response headers:', [...response.headers.entries()]);
      if (!response.ok) {
        throw new Error('Failed to update appointment status.');
      }

      // Parse the response
      const result = await response.json();
      const { status } = result;

      // Update the status in the table dynamically
      const row = document.querySelector(`tr[data-id='${appointmentId}']`);
      if (row) {
        const statusCell = row.querySelector("[data-status]");
        if (statusCell) {
          statusCell.innerText = status;
        }
      }

      alert(`Appointment ${appointmentId} has been approved.`);
    } catch (error) {
      console.error('Error approving appointment:', error);
      alert("Failed to approve appointment.");
    }
  } else {
    alert("Action canceled.");
  }
}


//Appointment Completed section
async function CompletedRow(appointmentId) {
  const userConfirm = confirm("Do you want to Complete this appointment?");
  if (userConfirm) {
    try {
      // Check if appointmentId is valid before making the request
      if (!appointmentId || isNaN(appointmentId)) {
        alert("Invalid appointment ID.");
        return;
      }
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      const response = await fetch(`http://127.0.0.1:8000/doctors/complete_appointment/${appointmentId}/`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': csrfToken,
         },
      });

      if (!response.ok) {
        throw new Error('Failed to update appointment status.');
      }

      // Update the status in the table after successful update
      const row = document.querySelector(`tr[data-id='${appointmentId}']`);
      if (row) {
        row.querySelector("td:nth-last-child(2)").innerText = "Completed"; 
      }

      alert(`Appointment ${appointmentId} has been Completed.`);
    } catch (error) {
      console.error('Error completing appointment:', error);
      alert("Failed to complete appointment.");
    }
  } else {
    alert("Action canceled.");
  }
}

//Appointment delete
async function deleteAppointment(appointmentId) {
  const userConfirm = confirm("Do you want to delete this appointment?");
  if (userConfirm) {
    try {
      // Check if appointmentId is valid before making the request
      if (!appointmentId || isNaN(appointmentId)) {
        alert("Invalid appointment ID.");
        return;
      }
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

      const response = await fetch(`http://127.0.0.1:8000/doctors/delete_appointment/${appointmentId}/`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': csrfToken, },
      });

      if (!response.ok) {
        throw new Error('Failed to delete appointment status.');
      }

      

      alert(`Appointment ${appointmentId} has been deleted.`);
    } catch (error) {
      console.error('Error deleting appointment:', error);
      alert("Failed to deleting appointment.");
    }
  } else {
    alert("Action canceled.");
  }
}


///Appointment Edit function

// Define `currentAppointmentId` globally
let currentDocAppointmentId = null;

// Function to handle editing an appointment
function editRow(id) {
  // Set the currentAppointmentId to the ID of the appointment being edited
  currentDocAppointmentId = id;
  console.log("Doctor Appointment Edit ID: ",currentDocAppointmentId);
 
}

document.getElementById("AppointmentDocEditForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission

  // Gather form data to send to the server
  const DocformDataEdit = {
    appointment_status: document.getElementById("appointmentStatusEdit").value,
    
    appointment_date: document.getElementById("appointmentDateEditDoc").value,
    appointment_time: document.getElementById("appointmentTimeEditDoc").value,
    communication_type: document.getElementById("communicationTypeEditDoc").value,
    payment_type: document.getElementById("paymentTypeEditDoc").value,
  };
  console.log("Sending data:", DocformDataEdit);

  // Use the stored `currentAppointmentId` in the URL
  fetch(`http://localhost:3000/doc/appointments/${currentDocAppointmentId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(DocformDataEdit), 
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert("Appointment updated successfully!");
      } else {
        alert("Failed to update the appointment. Please try again.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred while updating the appointment.");
    });
});



//API For deleting account
function deleteAccount() {
  const isConfirmedAcc = confirm("Are you sure you want to delete your account?");
  
  if (!isConfirmedAcc) {
    return;
  }

  fetch("http://localhost:3000/del/DocAccount", {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ doctor_id}) 
  })
    .then(response => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then(data => {
      console.log("Data fetched is:", data);
      alert("Account deleted successfully!");
      window.location.href = 'http://127.0.0.1:5500/portal.html';
    })
    .catch(error => {
      console.error("Fetching error:", error);
      alert("Failed to delete Account. Please try again.");
    });
}





// toggle section
// toggle sections

// Function to toggle the sliding panels
function toggleSlideDoc(contentIdDoc) { 
  // First, close any open panels and disable settings
  const allPanelsDoc = document.querySelectorAll('.slidingDocContent' );
  allPanelsDoc.forEach(panel => {
    panel.classList.remove('active');
  });

  // Then, toggle the clicked panel
  const contentDoc = document.getElementById(contentIdDoc);
  contentDoc.classList.toggle('active');

  // Close settings if it's open
  const settingsContentDoc = document.querySelector('.settingsDocContent');
  settingsContentDoc.classList.remove('active');
}

// Function to toggle the settings content
function toggleSettingsDoc() {
  // Close any open panels
  const allPanelsDoc = document.querySelectorAll('.slidingDocContent');
  allPanelsDoc.forEach(panel => {
    panel.classList.remove('active');
  });

  // Toggle the settings content
  const content2Doc = document.querySelector('.settingsDocContent');
  content2Doc.classList.toggle('active');
}

//For the appointment section
function toggle1(){
  
  var popup=document.getElementById('popupPat')
  popup.classList.toggle('active')
  var parent=document.querySelector('.TheContentPatContainer')
  parent.classList.toggle('active')

}

//for the appointment table section



 function toggle2(){
  var popup2=document.querySelector('.upcoming')
  popup2.classList.toggle('active')
  var parent=document.querySelector('.TheContentPatContainer')
  parent.classList.toggle('active')
}



//for account updates
 //for the appointment table section
function toggle4() {
  // Select the modal and parent div
  var popup3 = document.querySelector('.modalDoc');
  var parent = document.querySelector('.settingsDocContent');

  // Toggle the active class on the modal
  popup3.classList.toggle('active');

  // If the modal is active, add the blur effect to the parent and change its class to .blur
  if (popup3.classList.contains('active')) {
    parent.classList.add('blur');  // Add blur effect
    parent.classList.remove('active'); // Remove the active class, if necessary
  } else {
    parent.classList.remove('blur'); // Remove blur effect
    parent.classList.add('active');  // Add back active class, if necessary
  }
}


//Log out section

function logoutDoc() {
  // Remove user session from sessionStorage
  sessionStorage.removeItem('userSession'); 

  // Clear the cookie if used for session info
  document.cookie = 'userSession=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;';

  // Redirect to login page or home page
  window.location.href = 'http://127.0.0.1:8000/authentication/signIn/'; // or your homepage URL
}