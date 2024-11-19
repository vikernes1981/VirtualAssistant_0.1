import requests
from dotenv import load_dotenv
import os

load_dotenv()

def get_random_fact():
    api_url = "https://api.api-ninjas.com/v1/facts"
    api_key = os.getenv("FACTS_API_KEY")
    
    if not api_key:
        print("Error: Missing API key. Please set the FACTS_API_KEY in the .env file.")
        return "Error: Missing API key."

    headers = {
        "X-Api-Key": api_key  # Use the loaded API key
    }
    
    try:
        response = requests.get(api_url, headers=headers, timeout=10)  # Added a timeout for the request
        response.raise_for_status()  # Raise an error for bad status codes
        
        fact_data = response.json()
        if fact_data and isinstance(fact_data, list) and "fact" in fact_data[0]:
            return fact_data[0].get("fact", "No fact found.")
        else:
            return "No fact found."

    except requests.RequestException as req_err:
        print(f"Request error: {req_err}")
        return "Failed to fetch a fact due to a network error."
    except ValueError as json_err:
        print(f"JSON parsing error: {json_err}")
        return "There was an error processing the fact data."
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "An unexpected error occurred while fetching a fact."
