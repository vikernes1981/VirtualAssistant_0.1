import requests

def get_random_joke():
    url = "https://icanhazdadjoke.com/"
    headers = {
        "Accept": "application/json",
        "User-Agent": "My Joke Fetcher (https://github.com/vikernes1981/VirtualAssistant_0.1)"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)  # Added a timeout for the request
        response.raise_for_status()  # Raise an error for bad status codes
        joke_data = response.json()
        return joke_data.get("joke", "No joke found.")
    except requests.RequestException as req_err:
        print(f"Request error: {req_err}")
        return "Failed to fetch a joke due to a network error."
    except ValueError as json_err:
        print(f"JSON parsing error: {json_err}")
        return "There was an error processing the joke data."
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "An unexpected error occurred while fetching a joke."

