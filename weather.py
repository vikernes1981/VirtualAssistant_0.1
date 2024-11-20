from openai import OpenAI
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
weather_api_key = os.getenv("WEATHER_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def get_weather(city):
    """
    Fetch the weather forecast using OpenWeather API and enhance it with OpenAI.
    """
    if not weather_api_key:
        print("Error: API key is missing. Please set the WEATHER_API_KEY in the .env file.")
        return "Error: Missing API key.", "Σφάλμα: Λείπει το κλειδί API."

    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city,
        'appid': weather_api_key,
        'units': 'metric'
    }

    try:
        # Fetch weather data from OpenWeather API
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "cod" in data and data["cod"] == "200":
            if 'city' in data and 'list' in data:
                forecast = data['list'][0]  # Get the first forecast
                time = forecast.get('dt_txt', 'N/A')
                temp = forecast.get('main', {}).get('temp', 'N/A')
                description = forecast.get('weather', [{}])[0].get('description', 'N/A')

                # Use OpenAI to enhance the weather report
                enhanced_forecast = enhance_with_openai(city, time, temp, description)
                return enhanced_forecast, enhanced_forecast  # Return the same for both English and Greek for now
            else:
                return "Invalid data received from the weather service.", "Ελήφθη μη έγκυρη δομή δεδομένων από την υπηρεσία καιρού."
        else:
            error_message = data.get("message", "Unknown error occurred.")
            return f"Sorry, I couldn't find the forecast information for that location. Error: {error_message}", \
                   f"Λυπάμαι, δεν μπόρεσα να βρω πληροφορίες πρόβλεψης για αυτήν την τοποθεσία. Σφάλμα: {error_message}"
    except requests.RequestException as req_err:
        print(f"Request error: {req_err}")
        return "There was an error fetching the forecast. Please check your connection or try again later.", \
               "Υπήρξε σφάλμα κατά την αναζήτηση της πρόβλεψης. Ελέγξτε τη σύνδεσή σας ή προσπαθήστε ξανά αργότερα."
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "An unexpected error occurred while fetching the forecast.", "Προέκυψε απρόσμενο σφάλμα κατά την αναζήτηση των δεδομένων πρόβλεψης."

def enhance_with_openai(city, time, temp, description):
    """
    Use OpenAI to generate a sarcastic weather summary.
    """
    try:
        prompt = (
            f"Create a sarcastic weather report based on the following details:\n"
            f"City: {city}\n"
            f"Time: {time}\n"
            f"Temperature: {temp}°C\n"
            f"Description: {description}\n"
            f"Make it humorous, full of sarcasm, but still informative."
        )
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a humorous assistant creating sarcastic weather reports."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI error: {e}")
        return f"The weather in {city} is {description} with a temperature of {temp}°C. Try not to melt!"
