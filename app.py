from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__, templates_folder="Templates")

API_KEY = "d9a30d9b082d54530163a322216b4734"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.form.get("city").strip()
        if not city:
            error = "Please enter a city name!"
        else:
            URL = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(URL).json()

            if response.get("cod") == 200:
                weather_data = {
                    "city": response["name"],
                    "temp": response["main"]["temp"],
                    "weather": response["weather"][0]["description"].capitalize(),
                    "icon": response["weather"][0]["icon"],  # Weather icon code
                    "humidity": response["main"]["humidity"],
                    "wind_speed": response["wind"]["speed"],
                    "country": response["sys"]["country"],
                }
            else:
                error = f"City '{city}' not found!"

    return render_template("index.html", weather=weather_data, error=error)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port)
