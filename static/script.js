// Upon loading the page, if it's a first time user, we default to New York, otherwise, load
// their preferred location.
let userLocation = localStorage.getItem("default_location")

if (userLocation === null) {
    localStorage.setItem("default_location", "New York")
} 

// Updating default location text and current location
let locationText = document.getElementById("location")
locationText.textContent = localStorage.getItem("default_location")

let currentLocation = document.getElementById("curr-location")
currentLocation.textContent = localStorage.getItem("default_location")

let currentLocationSearch = userLocation

let defaultButton = document.getElementById("default")
defaultButton.addEventListener("click", changeDefault)

let searchBar = document.getElementById("search-input")
searchBar.value = "" // DEFAULT empty search bar

// Hourly and Weekly buttons
let hourlyButton = document.getElementById("hourly")
let weeklyButton = document.getElementById("weekly")
let hourlyTab = document.getElementById("hourly-content")
let weeklyTab = document.getElementById("weekly-content")

hourlyButton.addEventListener("click", toggleTimeFrame)
weeklyButton.addEventListener("click", toggleTimeFrame)

// Setting up weather for default location (Upon first load!) 
window.addEventListener("DOMContentLoaded", async () => {
    let result = await fetch(`/location?name=${currentLocation.textContent}`)
    let data = await result.json()
    console.log(data)
})

searchBar.addEventListener("keydown", search)
// TODO: add later functionality for when the magnifying glass is pressed

async function search(event) {
    if (event.key === "Enter") {
        let query = searchBar.value
        let result = await fetch(`/location?name=${query}`)
        let data = await result.json()
        console.log(data)

        if ('name' in data) {
            currentLocationSearch = data.name
            currentLocation.textContent = data.name
        }
    }
}

function changeDefault() {
    localStorage.setItem("default_location", currentLocationSearch)
    locationText.textContent = localStorage.getItem("default_location")
}

function toggleTimeFrame(event) {
    if ((event.target.id === "hourly" && weeklyTab.classList.contains("active")) || (event.target.id === "weekly" && hourlyTab.classList.contains("active"))) {
        hourlyTab.classList.toggle("active")
        weeklyTab.classList.toggle("active")
    }
}