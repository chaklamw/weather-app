// Upon loading the page, if it's a first time user, we default to New York, otherwise, load
// their preferred location.
let userLocation = localStorage.getItem("default_location")

if (userLocation === null) {
    localStorage.setItem("default_location", "New York")
} 

let locationText = document.getElementById("location")

locationText.textContent = "Location: " + localStorage.getItem("default_location")