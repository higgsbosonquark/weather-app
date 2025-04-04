from flask import Flask, render_template, request
import requests

app = Flask(__name__, template_folder="Templates")

API_KEY = "d9a30d9b082d54530163a322216b4734"  # Replace with your actual API key

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()

            if data.get("cod") == 200:
                weather_data = {
                    "city": city.title(),
                    "temperature": data["main"]["temp"],
                    "description": data["weather"][0]["description"].capitalize(),
                    "humidity": data["main"]["humidity"],
                    "wind_speed": data["wind"]["speed"],
                    "icon": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
                }
            else:
                error = "City not found. Please try again."

    return render_template("index.html", weather=weather_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
