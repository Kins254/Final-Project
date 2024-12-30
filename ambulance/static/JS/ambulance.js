function toggleMenu() {
    const menuInfo = document.querySelector('.menuInfo');
    menuInfo.classList.toggle('active');
  }
  

  function popUp(){
    const slide = document.querySelector(".loginPopUp");
    slide.classList.toggle("active");
    const slide2 = document.querySelector(".menuInfo");
    slide2.classList.toggle("blur");
  };
  

  //log in section
  document.querySelector(".form").addEventListener("submit", function (event) {
    event.preventDefault();
  
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
  
    fetch("http://127.0.0.1:5500/driver/login", { // Fixed URL
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: email,
        password: password,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network Response is not Ok"); // Fixed Error Constructor
        }
        return response.json();
      })
      .then((data) => {
        console.log("Fetched data is: ", data);
      })
      .catch((error) => {
        console.error("Fetching error:", error); // Properly log the error
      });
  });
  


//   // Assume Firebase is already initialized and imported
// import { getAuth } from 'firebase/auth';
// import { getDatabase, ref, set, onDisconnect, remove } from 'firebase/database';

// class OnlineStatusTracker {
//     constructor() {
//         this.onlineDiv = document.querySelector('.online');
//         this.onlineDetailDiv = document.querySelector('.onlineDetail');
//         this.auth = getAuth();
//         this.db = getDatabase();
//         this.locationTrackingInterval = null;
        
//         this.initializeEventListeners();
//     }

//     initializeEventListeners() {
//         this.onlineDiv.addEventListener('click', () => this.toggleOnlineStatus());
//     }

//     toggleOnlineStatus() {
//         // Check if user is logged in
//         const user = this.auth.currentUser;
        
//         if (!user) {
//             alert('Please log in to go online');
//             return;
//         }

//         if (this.locationTrackingInterval === null) {
//             this.startTracking(user);
//         } else {
//             this.stopTracking(user);
//         }
//     }

//     startTracking(user) {
//         // Update online status
//         this.onlineDetailDiv.querySelector('h3').textContent = 'Online';
        
//         // Start tracking location
//         this.locationTrackingInterval = setInterval(() => {
//             this.recordLocationAndTime(user);
//         }, 60000); // Update every minute

//         // Initial location record
//         this.recordLocationAndTime(user);

//         // Setup disconnect handling
//         const userStatusRef = ref(this.db, `users/${user.uid}/status`);
//         set(userStatusRef, {
//             state: 'online',
//             lastChanged: new Date().toISOString()
//         });

//         // Optional: Automatically set to offline if connection is lost
//         onDisconnect(userStatusRef).set({
//             state: 'offline',
//             lastChanged: new Date().toISOString()
//         });
//     }

//     stopTracking(user) {
//         // Clear interval
//         if (this.locationTrackingInterval !== null) {
//             clearInterval(this.locationTrackingInterval);
//             this.locationTrackingInterval = null;
//         }

//         // Update offline status
//         this.onlineDetailDiv.querySelector('h3').textContent = 'Offline';

//         // Remove from database
//         const userStatusRef = ref(this.db, `users/${user.uid}/status`);
//         remove(userStatusRef);
//     }

//     recordLocationAndTime(user) {
//         // Get current location
//         navigator.geolocation.getCurrentPosition(
//             (position) => {
//                 const locationRef = ref(this.db, `users/${user.uid}/locations`);
                
//                 set(locationRef, {
//                     latitude: position.coords.latitude,
//                     longitude: position.coords.longitude,
//                     timestamp: new Date().toISOString()
//                 });
//             },
//             (error) => {
//                 console.error('Error getting location', error);
//                 // Optionally handle location permission or error
//             }
//         );
//     }
// }

// // Initialize the tracker when the page loads
// document.addEventListener('DOMContentLoaded', () => {
//     new OnlineStatusTracker();
// });

// export default OnlineStatusTracker;