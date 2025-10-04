from flask import Flask, render_template
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

# Takes in a city name / zipcode, converts to longitude and latitude via Open-Meteo Geocoding API
def geocode(location):
    url=f"https://geocoding-api.open-meteo.com/v1/search?name={location}"
    
    response=requests.get(url)
    
    data=response.json()
    
    # Returns a tuple of latitude and longitude
    return (data["results"][0]["latitude"], data["results"][0]["longitude"])

if __name__ == "__main__":
    app.run(debug=True)