import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_weather(city):
    api_key = os.getenv("WEATHER_API_KEY")  # Load API key from .env file
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if data["cod"] == 200:
            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            city_name = data["name"]
            return f"The weather in {city_name} is {weather_description} with a temperature of {temperature}°C.", f"Ο καιρός στο {city_name} είναι {weather_description} με θερμοκρασία {temperature}°C."
        else:
            return "Sorry, I couldn't find the weather information for that location.", "Λυπάμαι, δεν μπόρεσα να βρω πληροφορίες καιρού για αυτήν την τοποθεσία."
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return "There was an error fetching the weather information.", "Υπήρξε σφάλμα κατά την αναζήτηση πληροφοριών καιρού."
