import os
from speech import speak, recognize_speech  # Import updated speech functions
from globals import current_language
from database import insert_dictated_text
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please ensure it's set in the .env file.")

def real_time_dictation(stop_word="τέλος"):
    text_output = ""
    try:
        speak("I am ready to start dictation.", "Είμαι έτοιμος να αρχίσω την υπαγόρευση. Πες 'τέλος' για να σταματήσεις.")
        print("Start speaking. Say 'τέλος' to stop or 'delete words' to remove specific words.")

        while True:
            # Capture and transcribe audio using recognize_speech()
            transcription = recognize_speech()

            if not transcription:
                print("No valid transcription received. Stopping dictation.")
                break

            # Check for stop word
            if stop_word in transcription:
                speak("Dictation stopped.", "Η υπαγόρευση σταμάτησε.")
                break
            elif "delete words" in transcription or "διαγραφή λέξεων" in transcription:
                speak("How many words do you want to delete?", "Πόσες λέξεις θέλεις να διαγράψεις;")
                try:
                    num_words = int(input("Enter the number of words to delete: "))
                    words = text_output.strip().split()
                    if len(words) >= num_words:
                        text_output = " ".join(words[:-num_words])
                        print(f"The last {num_words} words have been removed.")
                    else:
                        speak("Not enough words to delete.", "Δεν υπάρχουν αρκετές λέξεις για διαγραφή.")
                except ValueError:
                    speak("Invalid number.", "Μη έγκυρος αριθμός.")
            else:
                text_output += transcription + " "
                print(transcription, end=" ", flush=True)

    except Exception as e:
        print(f"Error during dictation: {e}")
        speak("An error occurred during dictation.", "Υπήρξε σφάλμα κατά την υπαγόρευση.")
        return ""

    # Store the text in the database
    if text_output.strip():
        language = 'gr' if current_language == 'gr' else 'en'
        try:
            if insert_dictated_text(text_output.strip(), language):
                speak("The text has been stored in the database.", "Το κείμενο αποθηκεύτηκε στη βάση δεδομένων.")
            else:
                speak("There was an error saving the text to the database.", "Υπήρξε σφάλμα κατά την αποθήκευση του κειμένου.")
        except Exception as e:
            print(f"Error saving text to the database: {e}")
            speak("There was an error while saving the text.", "Υπήρξε σφάλμα κατά την αποθήκευση του κειμένου.")

    return text_output
