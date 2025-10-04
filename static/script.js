// Upon loading the page, if it's a first time user, we default to New York, otherwise, load
// their preferred location.
let userLocation = localStorage.getItem("default_location")

if (userLocation === null) {
    localStorage.setItem("default_location", "New York")
} 

let locationText = document.getElementById("location")

locationText.textContent = localStorage.getItem("default_location")

let currentLocation = document.getElementById("curr-location")
currentLocation.textContent = localStorage.getItem("default_location")

let currentLocationSearch = userLocation

let defaultButton = document.getElementById("default")
defaultButton.addEventListener("click", changeDefault)

let searchBar = document.getElementById("search-input")
searchBar.value = "" // DEFAULT empty search bar

searchBar.addEventListener("keydown", search)
// TODO: add later functionality for when the magnifying glass is pressed

async function search(event) {
    if (event.key === "Enter") {
        let query = searchBar.value
        let result = await fetch(`/location?name=${query}`)
        let data = await result.json()

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