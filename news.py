import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_news():
    api_key = os.getenv("NEWS_API_KEY")  # Load API key from .env file
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        'country': 'us',  # Change to the desired country code
        'apiKey': api_key
    }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if data["status"] == "ok":
            articles = data["articles"][:5]  # Get the top 5 articles
            news_list_en = [f"{article['title']} - {article['source']['name']}" for article in articles]
            news_list_gr = [f"{article['title']} - {article['source']['name']}" for article in articles]  # Replace with Greek translations if available
            return "\n".join(news_list_en), "\n".join(news_list_gr)  # Return both English and Greek
        else:
            return "Sorry, I couldn't fetch the news at the moment.", "Λυπάμαι, δεν μπόρεσα να ανακτήσω τα νέα αυτή τη στιγμή."
    except Exception as e:
        print(f"Error fetching news: {e}")
        return "There was an error fetching the news.", "Υπήρξε σφάλμα κατά την αναζήτηση των ειδήσεων."
