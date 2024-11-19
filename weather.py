import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_weather(city):
    api_key = os.getenv("WEATHER_API_KEY")  # Load API key from .env file
    if not api_key:
        print("Error: API key is missing. Please set the WEATHER_API_KEY in the .env file.")
        return "Error: Missing API key.", "Σφάλμα: Λείπει το κλειδί API."

    base_url = "http://api.openweathermap.org/data/2.5/forecast"  # Endpoint for detailed forecast
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()

        if "cod" in data and data["cod"] == "200":
            if 'city' in data and 'list' in data:
                forecast_message = f"Here's the fucking weather forecast for fucking {data['city']['name']} throughout the fucking day:\n"
                greek_forecast_message = f"Η πρόβλεψη καιρού για το {data['city']['name']} κατά τη διάρκεια της ημέρας είναι:\n"
                if data['list']:
                    forecast = data['list'][0]  # Access the first forecast in the list
                    time = forecast.get('dt_txt', 'N/A')
                    temp = forecast.get('main', {}).get('temp', 'N/A')
                    description = forecast.get('weather', [{}])[0].get('description', 'N/A')
                    forecast_message += f"{time}: {description}, {temp}°C\n"
                    greek_forecast_message += f"{time}: {description}, {temp}°C\n"
                else:
                    forecast_message += "No fucking forecast data fucking available.\n"
                    greek_forecast_message += "Δεν υπάρχουν διαθέσιμα δεδομένα πρόβλεψης.\n"
                return forecast_message, greek_forecast_message
            else:
                return "Invalid fucking data structure fucking received from the fucking weather service.", "Ελήφθη μη έγκυρη δομή δεδομένων από την υπηρεσία καιρού."
        else:
            error_message = data.get("message", "Unknown error occurred.")
            return f"Sorry, I couldn't find the fucking forecast information for that fucking location. Error: {error_message}", \
                   f"Λυπάμαι, δεν μπόρεσα να βρω πληροφορίες πρόβλεψης για αυτήν την τοποθεσία. Σφάλμα: {error_message}"
    except requests.RequestException as req_err:
        print(f"Request error: {req_err}")
        return "There was a fucling error fetching the fucking forecast. Please check your fucking connection or fucking try again later.", \
               "Υπήρξε σφάλμα κατά την αναζήτηση της πρόβλεψης. Ελέγξτε τη σύνδεσή σας ή προσπαθήστε ξανά αργότερα."
    except ValueError as json_err:
        print(f"JSON error: {json_err}")
        return "There was a fucking error fucking processing the fucking forecast data.", "Υπήρξε σφάλμα κατά την επεξεργασία των δεδομένων πρόβλεψης."
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "A fucking unexpected error occurred while fucking fetching the fucking forecast.", "Προέκυψε απρόσμενο σφάλμα κατά την αναζήτηση των δεδομένων πρόβλεψης."
