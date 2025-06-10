# gpt_conversation.py

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    raise ValueError("Missing OPENAI_API_KEY in environment.")

client = OpenAI(api_key=openai_key)

def extract_intent_with_openai(user_input):
    try:
        system_prompt = (
            "You are a voice assistant. Extract the user's intent and any entities. "
            "Use one of the following intent names exactly: play_music, stop_music, "
            "add_note, view_notes, delete_note, dictate_text, help, weather, time, "
            "date, open_website, audiobook, set_volume, volume_up, volume_down, "
            "close_tab, greeting, farewell, delete_text. "
            "Respond ONLY in JSON. Example: {\"intent\": \"weather\", \"entities\": {\"location\": \"Berlin\"}}"
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content
        print("GPT raw response:", content)
        parsed = json.loads(content)
        intent = parsed.get("intent", "").strip()
        entities = parsed.get("entities", {})
        return intent, entities

    except Exception as e:
        print(f"[GPT ERROR] {e}")
        return None, {}
