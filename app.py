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

if __name__ == "__main__":
    app.run(debug=True)