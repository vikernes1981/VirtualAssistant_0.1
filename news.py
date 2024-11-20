import requests
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
news_api_key = os.getenv("NEWS_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def fetch_and_process_news():
    """
    Fetch news from NewsAPI, then use OpenAI to create a concise title and 15-word summary.
    Returns:
        list of tuples: [(title, summary), ...]
    """
    if not news_api_key:
        print("Error: Missing NewsAPI key. Please set the NEWS_API_KEY in the .env file.")
        return []

    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        'country': 'us',  # Change to your preferred country
        'apiKey': news_api_key
    }

    try:
        # Fetch articles from NewsAPI
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "ok":
            articles = data.get("articles", [])[:5]  # Get the top 5 articles
            processed_news = []
            for article in articles:
                # Extract details from the article
                original_title = article.get("title", "No Title")
                description = article.get("description", "No Description")

                # Generate a concise title and summary using OpenAI
                generated_title, summary = process_with_openai(original_title, description)
                processed_news.append((generated_title, summary))
            return processed_news
        else:
            error_message = data.get("message", "Unknown error occurred.")
            print(f"NewsAPI Error: {error_message}")
            return []
    except requests.RequestException as req_err:
        print(f"Request error: {req_err}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def process_with_openai(original_title, description):
    """
    Generate a concise title and 15-word summary using OpenAI.
    Args:
        original_title (str): The original title from NewsAPI.
        description (str): The description of the article from NewsAPI.
    Returns:
        tuple: (generated_title, summary)
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant summarizing news articles."},
                {"role": "user", "content": (
                    f"Create a concise title and a 15-word summary for the following news article:\n"
                    f"Original Title: {original_title}\n"
                    f"Description: {description}\n"
                )}
            ]
        )
        response = completion.choices[0].message.content.strip()
        lines = response.split("\n")
        
        if len(lines) >= 2:
            generated_title = lines[0].replace("Title: ", "").strip()
            summary = lines[1].replace("Summary: ", "").strip()
            return generated_title, summary
        else:
            return "Generated Title", "No summary could be generated."
    except Exception as e:
        print(f"OpenAI error: {e}")
        return "Generated Title", "An error occurred while generating the summary."

def display_news():
    """
    Fetch, process, and display the news.
    """
    news_list = fetch_and_process_news()
    if news_list:
        for idx, (title, summary) in enumerate(news_list, start=1):
            print(f"News {idx}:")
            print(f"  Title: {title}")
            print(f"  Summary: {summary}")
            print()
            speak(f"News {idx}: {title}. {summary}.", 
                  f"Νέα {idx}: {title}. {summary}.")
    else:
        print("No news articles available.")
