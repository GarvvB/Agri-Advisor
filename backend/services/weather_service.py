import requests

API_KEY = "31cf97395c3345078bf5aba79b214d52"  # <-- put your real key here

def get_weather(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=5)
        data = response.json()

        # If API fails, fallback to default safe weather
        if "main" not in data:
            return {
                "temperature": 28,
                "humidity": 65,
                "rainfall": 0
            }

        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "rainfall": data.get("rain", {}).get("1h", 0)
        }

    except Exception:
        # Fallback if internet/API fails
        return {
            "temperature": 28,
            "humidity": 65,
            "rainfall": 0
        }
