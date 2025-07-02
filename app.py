from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "96e7ec1adf813cba22fc64c9f28ef7cc"
WAQI_TOKEN = "336447b114bc6220f71dd1752af43b1f3ca3926f"

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
WAQI_URL = "https://api.waqi.info/feed/geo:{lat};{lon}/?token={token}"


def interpret_aqi(aqi):
    if aqi <= 50:
        return "Good 😊"
    elif aqi <= 100:
        return "Moderate 🙂"
    elif aqi <= 150:
        return "Unhealthy for Sensitive 😐"
    elif aqi <= 200:
        return "Unhealthy 😷"
    elif aqi <= 300:
        return "Very Unhealthy 😵"
    else:
        return "Hazardous ☠️"


@app.route("/", methods=["GET", "POST"])
def dashboard():
    data = None
    forecast = []
    chart_labels = []
    chart_temps = []

    if request.method == "POST":
        city = request.form.get("city")
        response = requests.get(f"{WEATHER_URL}?q={city}&appid={API_KEY}&units=metric")

        if response.status_code == 200:
            weather = response.json()
            lat, lon = weather["coord"]["lat"], weather["coord"]["lon"]

            # AQI Fetch via lat/lon
            aqi_value = "-"
            aqi_description = "Not available"
            try:
                aqi_response = requests.get(WAQI_URL.format(lat=lat, lon=lon, token=WAQI_TOKEN))
                aqi_json = aqi_response.json()
                if aqi_json["status"] == "ok":
                    aqi_value = aqi_json["data"]["aqi"]
                    aqi_description = interpret_aqi(aqi_value)
            except Exception as e:
                print("AQI fetch failed:", e)

            forecast_data = requests.get(f"{FORECAST_URL}?q={city}&appid={API_KEY}&units=metric").json()
            used_dates = set()

            for item in forecast_data["list"]:
                date, time = item["dt_txt"].split()
                if time == "12:00:00" and date not in used_dates:
                    temp = round(item["main"]["temp"])
                    description = item["weather"][0]["description"].title()
                    forecast.append({
                        "date": datetime.strptime(date, "%Y-%m-%d").strftime("%a, %b %d"),
                        "temp": temp,
                        "description": description,
                        "icon": item["weather"][0]["icon"]
                    })
                    chart_labels.append(datetime.strptime(date, "%Y-%m-%d").strftime("%a"))
                    chart_temps.append(temp)
                    used_dates.add(date)
                    if len(forecast) == 5:
                        break

            timezone_offset = weather["timezone"]
            sunrise = datetime.utcfromtimestamp(weather["sys"]["sunrise"] + timezone_offset).strftime("%I:%M %p")
            sunset = datetime.utcfromtimestamp(weather["sys"]["sunset"] + timezone_offset).strftime("%I:%M %p")

            data = {
                "city": city.title(),
                "temperature": round(weather["main"]["temp"]),
                "humidity": weather["main"]["humidity"],
                "description": weather["weather"][0]["description"].title(),
                "aqi": aqi_value,
                "aqi_description": aqi_description,
                "sunrise": sunrise,
                "sunset": sunset,
                "timezone": timezone_offset
            }

    return render_template("index.html", data=data, forecast=forecast,
                           labels=chart_labels, temps=chart_temps)


if __name__ == "__main__":
    app.run(debug=True)
