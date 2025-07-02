
# 🌤️ Weather Dashboard

A clean and responsive web application that allows users to get the current weather, 5-day forecast, AQI (Air Quality Index), and real-time time/date for any city using the OpenWeatherMap and WAQI APIs.

## 🚀 Features

- 🌡️ Current temperature, humidity, and weather description
- 🌅 Sunrise and 🌇 sunset times
- 🌫️ AQI value with emoji-based interpretation
- 📈 Interactive 5-day temperature forecast (line graph)
- 📋 Forecast table
- 🕒 Real-time clock & date (adjusted to city's timezone)
- 🔍 Search functionality with a clean, responsive UI

## 🛠️ Tech Stack

- Python (Flask)
- HTML5 / CSS3
- JavaScript (Chart.js)
- APIs:
  - [OpenWeatherMap](https://openweathermap.org/api)
  - [WAQI (World Air Quality Index)](https://aqicn.org/api/)

## 📸 Screenshot

![Screenshot of Weather Dashboard](in dashboard views)


## 🧑‍💻 Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/aditi758/weather_dashboard.git
   cd weather_dashboard
2. python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
3. API_KEY = "your_openweathermap_key"
    WAQI_TOKEN = "your_waqi_token"
4. python app.py


weather_dashboard/
├── app.py
├── static/
│   └── style.css
├── templates/
│   └── index.html
└── README.md



