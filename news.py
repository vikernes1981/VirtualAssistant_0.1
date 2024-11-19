import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_news():
    api_key = os.getenv("NEWS_API_KEY")  # Load API key from .env file
    if not api_key:
        print("Error: Missing API key. Please set the NEWS_API_KEY in the .env file.")
        return "Error: Missing API key.", "Σφάλμα: Λείπει το κλειδί API."

    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        'country': 'us',  # Change to the desired country code
        'apiKey': api_key
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()

        if data.get("status") == "ok":
            articles = data.get("articles", [])[:5]  # Get the top 5 articles if available
            if articles:
                news_list_en = [f"{article.get('title', 'No Title')} - {article.get('source', {}).get('name', 'Unknown Source')}" for article in articles]
                news_list_gr = [f"{article.get('title', 'No Title')} - {article.get('source', {}).get('name', 'Unknown Source')}" for article in articles]  # Replace with Greek translations if available
                return "\n".join(news_list_en), "\n".join(news_list_gr)
            else:
                return "No news articles were found.", "Δεν βρέθηκαν ειδήσεις."
        else:
            error_message = data.get("message", "Unknown error occurred.")
            return f"Sorry, I couldn't fetch the news. Error: {error_message}", f"Λυπάμαι, δεν μπόρεσα να ανακτήσω τα νέα. Σφάλμα: {error_message}"

    except requests.RequestException as req_err:
        print(f"Request error: {req_err}")
        return "There was an error fetching the news. Please check your connection or try again later.", "Υπήρξε σφάλμα κατά την αναζήτηση των ειδήσεων. Ελέγξτε τη σύνδεσή σας ή προσπαθήστε ξανά αργότερα."
    except ValueError as json_err:
        print(f"JSON error: {json_err}")
        return "There was an error processing the news data.", "Υπήρξε σφάλμα κατά την επεξεργασία των δεδομένων ειδήσεων."
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "An unexpected error occurred while fetching the news.", "Προέκυψε απρόσμενο σφάλμα κατά την αναζήτηση των ειδήσεων."
