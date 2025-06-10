"""
Provides integration with the Wit.ai API for intent detection.

Sends user input to Wit and extracts the top-ranked intent (if any).
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

WIT_API_KEY = os.getenv("WIT_API_KEY")
WIT_API_URL = "https://api.wit.ai/message"

if not WIT_API_KEY:
    raise ValueError("Missing WIT_API_KEY environment variable")


def get_intent_from_wit(text: str) -> str | None:
    """
    Send a text query to Wit.ai and extract the top intent name.

    Args:
        text (str): The user command.

    Returns:
        str | None: The top detected intent name, or None if none found.
    """
    headers = {
        "Authorization": f"Bearer {WIT_API_KEY}",
        "Content-Type": "application/json"
    }

    params = {"q": text}

    try:
        response = requests.get(WIT_API_URL, headers=headers, params=params, timeout=3)
        response.raise_for_status()
        data = response.json()
        print(f"[WIT] Response: {data}")

        intents = data.get("intents", [])
        if intents:
            return intents[0]["name"]

    except requests.exceptions.RequestException as e:
        print(f"[WIT ERROR] Request failed: {e}")
    except Exception as e:
        print(f"[WIT ERROR] {e}")

    return None
