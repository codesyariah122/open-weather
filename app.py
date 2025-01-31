import os
import requests
from flask import Flask, render_template, request
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

def get_city_coordinates(city):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    response = requests.get(geo_url)
    if response.status_code == 200 and response.json():
        data = response.json()[0]
        return data["lat"], data["lon"]
    return None, None

def get_weather_forecast(city):
    lat, lon = get_city_coordinates(city)
    if lat is None or lon is None:
        return None
    
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        forecast_data = []
        for item in data["list"]:
            forecast_data.append({
                "date": datetime.utcfromtimestamp(item["dt"]).strftime('%d %B %Y, %H:%M'),
                "temp": item["main"]["temp"],
                "humidity": item["main"]["humidity"],
                "description": item["weather"][0]["description"],
                "icon": item["weather"][0]["icon"]
            })
        return forecast_data[:7] 
    else:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    city = "Jakarta"

    if request.method == "POST":
        city = request.form.get("city")
    
    weather_data = get_weather_forecast(city)

    return render_template("index.html", weather_data=weather_data, city=city)

if __name__ == "__main__":
    app.run(debug=True)
