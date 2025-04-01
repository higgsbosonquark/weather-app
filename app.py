from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "d9a30d9b082d54530163a322216b4734"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error = None
    city = "Lucknow"  # Default city

    if request.method == "POST":
        city = request.form["city"]

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] == 200:
            weather_data = {
                "city": city.capitalize(),
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "description": data["weather"][0]["description"].capitalize(),
                "icon": data["weather"][0]["icon"],
            }
        else:
            error = "City not found! Please enter a valid city name."

    except Exception as e:
        error = "Error fetching weather data."

    return render_template("index.html", weather=weather_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
