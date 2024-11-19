import requests

def get_random_joke():
    url = "https://icanhazdadjoke.com/"
    headers = {
        "Accept": "application/json",
        "User-Agent": "My Joke Fetcher (https://github.com/yourusername)"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        joke_data = response.json()
        return joke_data.get("joke", "No joke found!")
    else:
        return "Failed to fetch a joke."
