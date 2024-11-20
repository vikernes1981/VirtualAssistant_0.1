import os
from openai import OpenAI
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def get_random_joke():
    """
    Fetch a random joke using icanhazdadjoke API or fallback to OpenAI.
    """
    # Step 1: Try fetching a joke from icanhazdadjoke API
    url = "https://icanhazdadjoke.com/"
    headers = {
        "Accept": "application/json",
        "User-Agent": "My Joke Fetcher (https://github.com/vikernes1981/VirtualAssistant_0.1)"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        joke_data = response.json()
        return joke_data.get("joke", "No joke found.")
    except requests.RequestException as req_err:
        print(f"API request error: {req_err}")
    except ValueError as json_err:
        print(f"JSON parsing error: {json_err}")
    except Exception as e:
        print(f"Unexpected error with API: {e}")

    # Step 2: Fallback to OpenAI
    print("Falling back to OpenAI for joke generation...")
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a humorous assistant. Generate a funny joke."},
                {"role": "user", "content": "Tell me a random joke."}
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI error: {e}")
        return "I couldn't fetch a joke. Sorry about that!"
