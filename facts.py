import requests
from dotenv import load_dotenv
import os
import openai

load_dotenv()

# Load API keys
facts_api_key = os.getenv("FACTS_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

def get_random_fact():
    """
    Fetch a random fact from the Ninjas Facts API or OpenAI as a fallback.
    Returns:
        str: A random fact or an error message.
    """
    api_url = "https://api.api-ninjas.com/v1/facts"

    if not facts_api_key:
        print("Error: Missing Ninjas Facts API key. Please set the FACTS_API_KEY in the .env file.")
        return "Error: Missing Ninjas Facts API key."

    headers = {
        "X-Api-Key": facts_api_key  # Use the loaded API key
    }
    
    try:
        # Try fetching a fact from the Ninjas Facts API
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
        
        fact_data = response.json()
        if fact_data and isinstance(fact_data, list) and "fact" in fact_data[0]:
            return fact_data[0].get("fact", "No fact found.")
        else:
            print("No fact found in API response. Falling back to OpenAI.")
            return get_fact_from_openai()

    except requests.RequestException as req_err:
        print(f"Request error: {req_err}")
        return get_fact_from_openai()  # Fallback to OpenAI
    except ValueError as json_err:
        print(f"JSON parsing error: {json_err}")
        return "There was an error processing the fact data."
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "An unexpected error occurred while fetching a fact."

def get_fact_from_openai():
    """
    Generate a fun fact using OpenAI if the Ninjas Facts API fails.
    Returns:
        str: A random fun fact.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant providing fun random facts."},
                {"role": "user", "content": "Give me a random fun fact."}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error using OpenAI for fallback: {e}")
        return "Failed to fetch a fact from both the API and OpenAI."
