"""
Fetches weather data using OpenWeatherMap and generates a sarcastic summary using GPT.
"""

import requests
import os
from dotenv import load_dotenv
from openai import OpenAI
from speech import speak
from globals import DEFAULT_WEATHER_CITY, GPT_MODEL

load_dotenv()
weather_api_key = os.getenv("WEATHER_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


def get_weather(city: str = DEFAULT_WEATHER_CITY) -> str:
    """
    Fetch weather data from OpenWeatherMap for the specified city
    and return a sarcastic summary via GPT.

    Args:
        city (str): The name of the city to fetch weather for.

    Returns:
        str: Sarcastic weather summary or fallback string.
    """
    if not weather_api_key:
        print("Missing WEATHER_API_KEY in .env.")
        return "Error: Missing weather API key."

    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": weather_api_key,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("cod") != "200" or not data.get("list"):
            return f"Couldn't fetch weather. API error: {data.get('message', 'unknown')}"

        forecast = data["list"][0]
        time_str = forecast.get("dt_txt", "N/A")
        temp = forecast.get("main", {}).get("temp", "N/A")
        desc = forecast.get("weather", [{}])[0].get("description", "N/A")

        # Get sarcastic summary and display it clearly
        summary = enhance_with_openai(city, time_str, temp, desc)

        print("\n" + "=" * 50)
        print("🌦️  Sarcastic Weather Forecast")
        print("-" * 50)
        print(summary)
        print("=" * 50 + "\n")


        return summary

    except requests.RequestException as e:
        print(f"Weather API error: {e}")
        return "Couldn't fetch the weather. Try again later."
    except Exception as e:
        print(f"Unexpected weather error: {e}")
        return "An error occurred while processing the forecast."



def enhance_with_openai(city: str, time: str, temp: float, description: str) -> str:
    """
    Use GPT to create a sarcastic weather report based on raw forecast data.

    Args:
        city (str): The city name.
        time (str): Forecast time.
        temp (float): Temperature in Celsius.
        description (str): Weather description.

    Returns:
        str: A GPT-generated sarcastic weather report.
    """
    try:
        prompt = (
            f"Create a sarcastic weather report:\n"
            f"City: {city}\n"
            f"Time: {time}\n"
            f"Temperature: {temp}°C\n"
            f"Description: {description}\n"
            f"Make it funny and sarcastic."
        )

        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": "You are a sarcastic weather assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"OpenAI error: {e}")
        return f"The weather in {city} is {description}, {temp}°C. Try not to melt."
