import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_weather(city):
    api_key = os.getenv("WEATHER_API_KEY")  # Load API key from .env file
    base_url = "http://api.openweathermap.org/data/2.5/forecast"  # Endpoint for detailed forecast
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if data["cod"] == "200":
            forecast_message = f"Here's the weather forecast for {data['city']['name']} throughout the day:\n"
            greek_forecast_message = f"Η πρόβλεψη καιρού για το {data['city']['name']} κατά τη διάρκεια της ημέρας είναι:\n"
            for forecast in data['list'][:1]:  # Limiting to 8 results (covering 24 hours in 3-hour intervals)
                time = forecast['dt_txt']
                temp = forecast['main']['temp']
                description = forecast['weather'][0]['description']
                forecast_message += f"{time}: {description}, {temp}°C\n"
                greek_forecast_message += f"{time}: {description}, {temp}°C\n"
            return forecast_message, greek_forecast_message
        else:
            return "Sorry, I couldn't find the forecast information for that location.", "Λυπάμαι, δεν μπόρεσα να βρω πληροφορίες πρόβλεψης για αυτήν την τοποθεσία."
    except Exception as e:
        print(f"Error fetching forecast: {e}")
        return "There was an error fetching the forecast information.", "Υπήρξε σφάλμα κατά την αναζήτηση πληροφοριών πρόβλεψης."
