from flask import Flask, render_template, request, jsonify
import openmeteo_requests
import pandas as pd
import requests
import requests_cache
from retry_requests import retry

# creation of Flask object, deals with interacting with the web
app = Flask(__name__)

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Think of this as an event listener (ex. button on click listeners in Kotlin), when we load the
# home page, then this function runs.
@app.route("/")
def home():
    return render_template("index.html")

# Each time enter is pressed on the search bar in the homepage, this will run geocode to convert
# the query into a location. This does NOT check if its a valid location. That is done in script.js
@app.route("/location")
def query():
    result = geocode(request.args.get("name"))
    
    if result is None:
        return jsonify({"error": "not found"})
    
    weather_information = get_weather(result[0],result[1])
    
    # Returns a json object to unpack in script.js, latitude, longitude, and the name of location
    return jsonify({
        "latitude": result[0],
        "longitude": result[1],
        "name": result[2]
    })

# Takes in a city name / zipcode, converts to longitude and latitude via Open-Meteo Geocoding API
def geocode(location):
    url=f"https://geocoding-api.open-meteo.com/v1/search?name={location}"
    
    response=requests.get(url)
    
    data=response.json()
    
    if ("error" in data or "results" not in data or len(data["results"]) == 0):
        return None
    
    # Returns a tuple of latitude and longitude and name
    return (data["results"][0]["latitude"], data["results"][0]["longitude"], data["results"][0]["name"])

# Takes in latitude and longitude, grabs weather information via Open-Meteo
def get_weather(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
	"latitude": latitude,
	"longitude": longitude,
	"daily": ["sunrise", "sunset","precipitation_probability_max"],
	"hourly": ["temperature_2m", "apparent_temperature", "rain", "showers", "snowfall"],
	"current": ["rain", "showers", "apparent_temperature", "snowfall", "temperature_2m", "precipitation"],
	"timezone": "auto",
    }
    responses = openmeteo.weather_api(url, params=params)
    
    response = responses[0]
    timezone = response.Timezone()
    timezoneABR = response.TimezoneAbbreviation()
    timezoneGMT = response.UtcOffsetSeconds()

    #  Process current data. The order of variables needs to be the same as requested.
    current = response.Current()
    current_rain = current.Variables(0).Value()
    current_showers = current.Variables(1).Value()
    current_apparent_temperature = current.Variables(2).Value()
    current_snowfall = current.Variables(3).Value()
    current_temperature_2m = current.Variables(4).Value()
    current_precipitation = current.Variables(5).Value()
    
    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(1).ValuesAsNumpy()
    hourly_rain = hourly.Variables(2).ValuesAsNumpy()
    hourly_showers = hourly.Variables(3).ValuesAsNumpy()
    hourly_snowfall = hourly.Variables(4).ValuesAsNumpy()

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_sunrise = daily.Variables(0).ValuesInt64AsNumpy()
    daily_sunset = daily.Variables(1).ValuesInt64AsNumpy()
    daily_precipitation_probability_max = daily.Variables(2).ValuesAsNumpy()
    
    return

if __name__ == "__main__":
    app.run(debug=True)