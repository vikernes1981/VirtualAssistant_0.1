from speech import recognize_speech, speak
from database import insert_note, get_all_notes, delete_note_by_id
from dotenv import load_dotenv
import os
import requests
from openai import OpenAI

# Load environment variables
load_dotenv()
wit_ai_token = os.getenv("WIT_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Set up OpenAI client
client = OpenAI(api_key=openai_api_key)

if not wit_ai_token or not openai_api_key:
    raise ValueError("Please ensure both WIT_AI_TOKEN and OPENAI_API_KEY are set in the .env file.")

def recognize_intent_with_wit(transcription):
    """
    Recognize intent using Wit.ai.
    Args:
        transcription (str): The user's transcribed speech.
    Returns:
        str: The recognized intent or None.
    """
    url = "https://api.wit.ai/message"
    headers = {
        "Authorization": f"Bearer {wit_ai_token}"
    }
    params = {"q": transcription}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        result = response.json()
        if "intents" in result and len(result["intents"]) > 0:
            return result["intents"][0]["name"]
        else:
            return None
    except requests.RequestException as e:
        print(f"Wit.ai request error: {e}")
        return None

def interpret_with_openai(transcription):
    """
    Fallback to OpenAI to interpret user intent when Wit.ai fails.
    Args:
        transcription (str): The user's transcribed speech.
    Returns:
        str: The interpreted action or response.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an intelligent assistant. Interpret user commands."},
                {"role": "user", "content": f"The user said: '{transcription}'. What is the user requesting?"}
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI error: {e}")
        return "I'm sorry, I couldn't interpret that."

# Include the number_map for recognizing words as numbers
number_map = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "1": 1, "2": 2, "3": 3, "4": 4, "5": 5,
    "6": 6, "7": 7, "8": 8, "9": 9, "10": 10
}

def process_user_command():
    """
    Ask the user what they want to do and handle their request.
    After completing a task, ask if they want to perform another task or exit.
    """
    while True:
        speak("What would you like to do? Add a note, view all notes, or delete a note?",
              "Τι θα ήθελες να κάνεις; Να προσθέσεις σημείωση, να δεις όλες τις σημειώσεις ή να διαγράψεις μια σημείωση;")
        
        print("Listening for your response...")
        transcription = recognize_speech()
        if not transcription:
            speak("I didn't catch that. Please try again.", "Δεν το κατάλαβα. Παρακαλώ προσπάθησε ξανά.")
            continue

        print(f"Transcription: {transcription}")

        # Step 1: Recognize intent using Wit.ai
        intent = recognize_intent_with_wit(transcription)
        if not intent:
            print("Wit.ai failed to recognize intent. Falling back to OpenAI.")
            intent = interpret_with_openai(transcription)

        # Step 2: Handle the recognized intent
        if intent == "add_note":
            while True:
                speak("Please say the note you'd like to add.", "Πες τη σημείωση που θέλεις να προσθέσεις.")
                note_content = recognize_speech()
                if note_content:
                    if insert_note(note_content):
                        speak("Note added successfully.", "Η σημείωση προστέθηκε με επιτυχία.")
                    else:
                        speak("There was an error adding the note.", "Υπήρξε σφάλμα κατά την προσθήκη της σημείωσης.")
                speak("Would you like to add another note or exit?", "Θέλεις να προσθέσεις άλλη σημείωση ή να αποχωρήσεις;")
                continue_response = recognize_speech()
                if continue_response and ("exit" in continue_response.lower() or "αποχωρώ" in continue_response.lower()):
                    return
        elif intent == "view_notes":
            while True:
                notes = get_all_notes()
                if notes:
                    print("Here are your notes:")
                    for idx, note in enumerate(notes, start=1):
                        print(f"Note {idx}: {note[1]}")
                    speak("Would you like to view your notes again or exit?",
                          "Θέλεις να δεις τις σημειώσεις σου ξανά ή να αποχωρήσεις;")
                    continue_response = recognize_speech()
                    if continue_response and ("exit" in continue_response.lower() or "αποχωρώ" in continue_response.lower()):
                        return
                else:
                    speak("You have no notes.", "Δεν έχεις σημειώσεις.")
                    return
        elif intent == "delete_note":
            while True:
                notes = get_all_notes()
                if notes:
                    print("Here are your notes:")
                    for idx, note in enumerate(notes, start=1):
                        print(f"Note {idx}: {note[1]}")
                    speak("Please say the number of the note you'd like to delete.",
                          "Πες τον αριθμό της σημείωσης που θέλεις να διαγράψεις.")
                    note_number = recognize_speech()
                    
                    # Handle number strings like "seven"
                    note_number = number_map.get(note_number.lower(), note_number)
                    
                    if isinstance(note_number, int) and 1 <= note_number <= len(notes):
                        note_index = note_number - 1
                        if delete_note_by_id(notes[note_index][0]):
                            speak("Note deleted successfully.", "Η σημείωση διαγράφηκε με επιτυχία.")
                        else:
                            speak("There was an error deleting the note.", "Υπήρξε σφάλμα κατά τη διαγραφή της σημείωσης.")
                    else:
                        speak("Invalid note number. Please try again.", "Μη έγκυρος αριθμός σημείωσης. Παρακαλώ προσπάθησε ξανά.")
                    speak("Would you like to delete another note or exit?", 
                          "Θέλεις να διαγράψεις άλλη σημείωση ή να αποχωρήσεις;")
                    continue_response = recognize_speech()
                    if continue_response and ("exit" in continue_response.lower() or "αποχωρώ" in continue_response.lower()):
                        return
                else:
                    speak("You have no notes to delete.", "Δεν έχεις σημειώσεις για διαγραφή.")
                    return
        else:
            speak("I'm sorry, I didn't understand what you want to do.", 
                  "Λυπάμαι, δεν κατάλαβα τι θέλεις να κάνεις.")

        # Ask if the user wants to perform another action
        speak("Would you like to perform another action or exit?", "Θέλεις να κάνεις άλλη ενέργεια ή να αποχωρήσεις;")
        continue_response = recognize_speech()
        if continue_response and ("exit" in continue_response.lower() or "αποχωρώ" in continue_response.lower()):
            return
