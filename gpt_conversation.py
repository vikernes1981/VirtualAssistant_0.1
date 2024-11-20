from speech import recognize_speech, speak
from process_commands import process_command
from openai import OpenAI
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def default_gpt_mode():
    """
    Default behavior: Handle intents or talk with GPT.
    """
    print("Assistant is ready.")

    while True:
        # Step 1: Listen for user command
        print("Listening for a command...")
        transcription = recognize_speech()
        if not transcription:
            speak("I didn't catch that. Please try again.", "Δεν το κατάλαβα. Παρακαλώ προσπάθησε ξανά.")
            continue

        print(f"Command: {transcription}")

        # Step 2: Check for intent
        intent = process_command(transcription)
        if intent:
            # If an intent is found, execute the corresponding action
            print(f"Intent detected: {intent}")
            continue  # Return to listening for the next command after processing

        # Step 3: Fallback to GPT for natural conversation
        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a friendly and conversational assistant."},
                    {"role": "user", "content": transcription}
                ]
            )
            gpt_response = completion.choices[0].message.content.strip()
            print(f"GPT: {gpt_response}")
            speak(gpt_response)

            # Short delay after speaking to prevent self-trigger
            time.sleep(1.5)

        except Exception as e:
            print(f"OpenAI error: {e}")
            speak("Sorry, I couldn't process your request.", "Λυπάμαι, δεν μπόρεσα να επεξεργαστώ το αίτημά σου.")
