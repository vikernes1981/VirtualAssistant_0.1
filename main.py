"""
Main entry point for the Virtual Assistant.

Initializes the system and enters a loop that listens for a wake word,
records user speech, detects intents, and routes commands accordingly.
"""

from globals import WAKE_WORD_MODEL_PATH
from speech import speak, recognize_speech
from wake_word import listen_for_wake_word
from process_commands import handle_intent
from database import initialize_database
from wit_conversation import extract_intent_and_entities
from fallback_handler import handle_unknown


if __name__ == "__main__":
    try:
        initialize_database()
    except Exception as e:
        print(f"Error initializing the database: {e}")
        speak("There was an error initializing the database.")

    while True:
        try:
            # Wait for wake word trigger
            listen_for_wake_word(WAKE_WORD_MODEL_PATH)

            # Visual log divider for clarity
            print("\n" + "=" * 60)
            print("🟢 New Wake Word Triggered — Listening for Intent")
            print("=" * 60 + "\n")

            speak("Ahoy.")

            # Capture user speech
            user_input = recognize_speech()
            if not user_input:
                continue

            # Try keyword override before invoking AI
            if handle_unknown(None, user_input, override=True):
                continue

            # Extract intent and entities using Wit.ai and fallback methods
            intent, entities = extract_intent_and_entities(user_input)
            

            # Route to handler
            handle_intent(intent, entities, user_input)

        except KeyboardInterrupt:
            speak("Goodbye.")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            speak("An unexpected error occurred.")
