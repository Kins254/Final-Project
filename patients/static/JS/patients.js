//setting the patient_id
const sessionData = document.getElementById('session-data');
const userType = sessionData.dataset.userType;
let patient_id = null;
let first_name = null;

if(userType==="patients"){
   patient_id = sessionData.dataset.patientId;
   first_name = sessionData.dataset.firstName;


}
else{
   patient_id = null;
   first_name = null;
}

console.log("Type In patient section:", userType);
console.log("Patient Id:", patient_id);
console.log("Patient's First name:", first_name);
/*
window.handleUserSession = function(userData) {
  // Store patient-specific session information
  sessionStorage.setItem('userId', userData.user_id);
  sessionStorage.setItem('userType', userData.user_type);
  sessionStorage.setItem('email', userData.email);
  sessionStorage.setItem('firstName', userData.first_name);
  sessionStorage.setItem('lastName', userData.last_name);
  console.log(`patient id is {userId}`)

  const patient_id = sessionStorage.getItem('userId');
  //const patient_id = 2;
  const first_name = sessionStorage.getItem('firstName');
  console.log(`Patient ID is ${patient_id}`);
  console.log(`Patient first name is ${first_name}`);
  // Additional patient-specific session handling
  console.log('Patient session initialized');
}
  */
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


//function to book an appointment
document.getElementById("appointmentForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission

    const doctorMapping = {
      "dr-smith": "01",
      "dr-johnson": "02",
      "dr-williams": "03",
    };

    const selectedDoctor = document.getElementById("doctor").value;
    console.log("Selected Doctor:", selectedDoctor);
    
    const formData = {
      appointment_type: document.getElementById("appointmentType").value,
      doctor_id: doctorMapping[selectedDoctor],
      appointment_date: document.getElementById("appointmentDate").value,
      appointment_time: document.getElementById("appointmentTime").value,
      communication_type: document.getElementById("communicationType").value,
      payment_type: document.getElementById("paymentType").value,
      patient_id: patient_id,
    };
    console.log("Sending data:", formData);

    fetch("http://127.0.0.1:3000/appointments", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert("Appointment booked successfully!");
        } else {
          alert("Failed to book the appointment. Please try again.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("An error occurred while booking the appointment.");
      });
  });

// Function to fetch appointments and populate the table
// Function to fetch appointments and populate the table()


async function fetchAppointments() {
  try {
   
    const response = await fetch(`http://localhost:3000/api/appointments/${patient_id}`);
    const appointments = await response.json();
    console.log("Appointment Data:", appointments);
    const tbody = document.getElementById("Tbody");
    tbody.innerHTML = ""; // Clear existing rows
    appointments.forEach((appointment) => {
      const row = document.createElement("tr");
      row.setAttribute("data-id", appointment.id);
      // Populate row with appointment data
      row.innerHTML = `
        <td>${appointment.id}</td>
        <td>${appointment.doctor_id}</td>
        <td>${appointment.appointment_date}</td>
        <td>${appointment.appointment_time}</td>
        <td>${appointment.appointment_type}</td>
        <td>${appointment.communication_type}</td>
        <td>${appointment.payment_type}</td>
        <td>
          <button class="edit-btnPat" onclick="editRowPat(${appointment.id}); showDiv()">Edit</button>
          <button class="delete-btnPat" onclick="deleteAppointmentPat(${appointment.id})">Delete</button>
        </td>
      `;
      tbody.appendChild(row);
    });
  } catch (error) {
    console.error("Error fetching appointments:", error);
  }
}

// Call the fetchAppointments function when the DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  console.log("Page loaded. Calling fetchAppointments.");
  fetchAppointments();
});

  //Function to toggle the edit section
  let currentPatAppointmentId = null;

  function editRowPat(id) {
    currentPatAppointmentId = id; // Set the ID globally
    console.log("Appointment Edit ID: ", currentPatAppointmentId);
  }
  
  function showDiv() {
    const popup4 = document.getElementById("EditSection");
    popup4.classList.toggle('active'); // Toggle visibility
  
    const blur2 = document.querySelector(".upcoming");
    if (popup4.classList.contains('active')) {
      blur2.classList.add('blur');   // Apply blur effect
      blur2.classList.remove('active');
    } else {
      blur2.classList.remove('blur'); // Remove blur effect
      blur2.classList.add('active');
    }
  }
  

// Function to handle updating the appointment

document.getElementById("AppointmentEditForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission

    const doctorMapping = {
      "dr-smith": "01",
      "dr-johnson": "02",
      "dr-williams": "03",
    };


    // Retrieve the patient ID from local storage (if necessary)
  
  const selectedDoctor = document.getElementById("doctorEdit").value;

  // Gather form data to send to the server
  const formDataEdit = {
    appointment_type: document.getElementById("appointmentTypeEdit").value,
    doctor_id: doctorMapping[selectedDoctor],
    appointment_date: document.getElementById("appointmentDateEdit").value,
    appointment_time: document.getElementById("appointmentTimeEdit").value,
    communication_type: document.getElementById("communicationTypeEdit").value,
    payment_type: document.getElementById("paymentTypeEdit").value,
  };
  console.log("Sending data:", formDataEdit);

  // Use the stored `currentAppointmentId` in the URL
  fetch(`http://localhost:3000/appointments/${currentPatAppointmentId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formDataEdit), 
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

//Function to delete appointments
let deletePatAppointmentId = null;

function deleteAppointmentPat(id) {
  deletePatAppointmentId = id;
  console.log("Delete Button appointment Id:", deletePatAppointmentId);

  // Show confirmation dialog
  const isConfirmed = confirm("Are you sure you want to delete this appointment?");
  
  // If user clicks Cancel, return early and do nothing
  if (!isConfirmed) {
    return;
  }

  // If user clicks OK, proceed with deletion
  fetch("http://localhost:3000/delete/patient/appointment", {
    method: "DELETE",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ id: deletePatAppointmentId })
  })
  .then(response => {
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return response.json();
  })
  .then(data => {
    console.log("Data fetched is:", data);
    // Show success message
    alert("Appointment deleted successfully!");
    // Refresh the appointments list
    fetchAppointments();
  })
  .catch(error => {
    console.error("Fetching error:", error);
    // Show error message
    alert("Failed to delete appointment. Please try again.");
  });
}

//Ambulance section
async function getUserLocationAndTime() {
  try {
      // Get current time
      const currentTime = new Date();
      const timeData = {
          localTime: currentTime.toLocaleTimeString(),
          localDate: currentTime.toLocaleDateString(),
          timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
          timestamp: currentTime.getTime()
      };

      // Get location using Geolocation API
      const locationData = await new Promise((resolve, reject) => {
          if (!navigator.geolocation) {
              reject(new Error('Geolocation is not supported by this browser.'));
          }

          navigator.geolocation.getCurrentPosition(
              (position) => {
                  resolve({
                      latitude: position.coords.latitude,
                      longitude: position.coords.longitude,
                      accuracy: position.coords.accuracy,
                      altitude: position.coords.altitude,
                      altitudeAccuracy: position.coords.altitudeAccuracy,
                      heading: position.coords.heading,
                      speed: position.coords.speed
                  });
              },
              (error) => {
                  reject(new Error(`Failed to get location: ${error.message}`));
              },
              {
                  enableHighAccuracy: true,
                  timeout: 5000,
                  maximumAge: 0
              }
          );
      });

      return {
          success: true,
          time: timeData,
          location: locationData
      };
  } catch (error) {
      return {
          success: false,
          error: error.message,
          time: null,
          location: null
      };
  }
}

// Add click event listener to ambulance parent element
document.querySelector('.ambulanceParent').addEventListener('click', async function() {
  const textElement = document.getElementById('text');
  textElement.textContent = "Searching For An Ambulance...";
  
  try {
      // Get user location and time
      const result = await getUserLocationAndTime();
      
      if (result.success) {
          // You can add additional logic here to:
          // 1. Send location to a server
          // 2. Calculate nearest ambulance
          // 3. Initiate emergency response
          
          console.log('Emergency request details:', {
              location: result.location,
              time: result.time
          });

          // Fixed fetch call
          const response = await fetch('/Ambulance/patient', {
              method: 'POST',
              headers: {  
                  'Content-Type': 'application/json'  
              },
              body: JSON.stringify({  
                  location: result.location,
                  time: result.time
              })
          });

          if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
          }

          const data = await response.json();
          console.log('Data fetched is: ', data);
          textElement.textContent = "Ambulance has been notified and is on the way!";
          
      } else {
          // Location access failed
          alert('Unable to find location. Please enable location services.');
          
          console.error('Location error:', result.error);
      }
  } catch (error) {
      // Handle any unexpected errors
      alert('An error occurred while searching for ambulance.')
    
      console.error('Error:', error);
  }
});


///function to edit the account details
// Function to edit account details
document
  .getElementById("updateAccountForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the form from submitting

    // Clear previous error messages
    document
      .querySelectorAll(".errorEdit")
      .forEach((span) => (span.textContent = ""));

    let isValid = true;

    // Validate Email
    const newEmail = document.getElementById("newEmail").value.trim();
    const newEmailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (newEmail === "") {
      document.getElementById("emailEdit").textContent = "Email is required.";
      isValid = false;
    } else if (!newEmailPattern.test(newEmail)) {
      document.getElementById("emailEdit").textContent =
        "Invalid email format.";
      isValid = false;
    }

    // validate current password
    const ConfirmPassword = document.getElementById("currentPassword").value;
    if (ConfirmPassword === "") {
      document.getElementById("currentPasswordEdit").textContent =
        "Password is required.";
    } else if (ConfirmPassword.length < 8) {
      document.getElementById("currentPasswordEdit").textContent =
        "Password must be at least 8 characters long.";
      isValid = false;
    }

    // Validate New Password
    const newPassword = document.getElementById("newPassword").value;
    if (newPassword === "") {
      document.getElementById("newPasswordEdit").textContent =
        "Password is required.";
      isValid = false;
    } else if (newPassword.length < 8) {
      document.getElementById("newPasswordEdit").textContent =
        "Password must be at least 8 characters long.";
      isValid = false;
    }

    // Validate Confirm Password
    const confirmPassword = document.getElementById("confirmPassword").value;
    if (confirmPassword === "") {
      document.getElementById("confirmPasswordError").textContent =
        "Confirm Password is required.";
      isValid = false;
    } else if (confirmPassword !== newPassword) {
      document.getElementById("confirmPasswordError").textContent =
        "Passwords do not match.";
      isValid = false;
    }
    const userId = sessionStorage.getItem('userId');
    if (isValid) {
      const data2 = {
        email: newEmail,
        password: ConfirmPassword,
        newpassword: newPassword,
        userId:patient_id
      };
      console.log("Sending data:", data2);

      fetch("http://localhost:3000/AccountEdit", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data2),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response is not OK");
          } else {
            return response.json();
          }
        })
        .then((data2) => {
          if (data2.success) {
            alert("Credentials updated successfully");
          } else {
            alert("Credentials update failed");
          }
        })
        .catch((error) => {
          console.error("Updating error:", error);
        });
    }
  });

//API For deleting account
document.querySelector(".DeleteAccountPat").addEventListener('click',function(){
  const isConfirmedAcc = confirm("Are you sure you want to delete your account?");
  
  // If user clicks Cancel, return early and do nothing
  if (!isConfirmedAcc) {
    return;
  }
  fetch("http://localhost:3000/del/patAccount",{
    method:'DELETE',
    headers:{'Content-Type':'application/JSON'},
    body:JSON.stringify({patient_id})
  })
  .then(response => {
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return response.json();
  })
  .then(data => {
    console.log("Data fetched is:", data);
    // Show success message
    alert("Account deleted successfully!");
    window.location.href = 'http://127.0.0.1:5500/portal.html'; // or your homepage URL
  
    
  })
  .catch(error => {
    console.error("Fetching error:", error);
    // Show error message
    alert("Failed to delete Account. Please try again.");
  });
});



  // toggle sections

// Function to toggle the sliding panels
function toggleSlidePat(contentIdPat) { 
  // First, close any open panels and disable settings
  const allPanelsPat = document.querySelectorAll('.slidingPatContent' );
  allPanelsPat.forEach(panel => {
    panel.classList.remove('active');
  });

  // Then, toggle the clicked panel
  const contentPat = document.getElementById(contentIdPat);
  contentPat.classList.toggle('active');

  // Close settings if it's open
  const settingsContentPat = document.querySelector('.settingsContent');
  settingsContentPat.classList.remove('active');
}

// Function to toggle the settings content
function toggleSettingsPat() {
  // Close any open panels
  const allPanelsPat = document.querySelectorAll('.slidingPatContent');
  allPanelsPat.forEach(panel => {
    panel.classList.remove('active');
  });

  // Toggle the settings content
  const content2Pat = document.querySelector('.settingsPatContent');
  content2Pat.classList.toggle('active');
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
function toggle3() {
  // Select the modal and parent div
  var popup3 = document.querySelector('.modal');
  var parent = document.querySelector('.settingsPatContent');

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
//first trial
document.getElementById('logoutPat').addEventListener('click', function() {
// Remove user session from localStorage
sessionStorage.removeItem('userSession'); 

// If you're using cookies to store session info, clear the cookie
document.cookie = 'userSession=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;'; // Clear the cookie

// Redirect to login page or home page
window.location.href = 'http://127.0.0.1:8000/authentication/signIn/'; // or your homepage URL
});