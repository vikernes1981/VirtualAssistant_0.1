from globals import current_language, recognizer  # Import global variables
from speech import speak, recognize_speech
from wake_word import listen_for_wake_word
from database import create_feedback_table
from process_commands import process_command

if __name__ == "__main__":
    try:
        create_feedback_table()  # Initialize the database if needed
    except Exception as e:
        print(f"Error initializing the database: {e}")
        speak("There was an error initializing the database.", "Υπήρξε σφάλμα κατά την αρχικοποίηση της βάσης δεδομένων.")
    
    while True:  # Keep the assistant running
        try:
            listen_for_wake_word("jarvis_linux.ppn")  # Use the wake word file (replace as needed)
            speak("Hello!", "Γεια σου!")  # Greet the user
            user_input = recognize_speech()  # Get user input
            if user_input:
                try:
                    process_command(user_input)  # Process the user's command
                except Exception as e:
                    print(f"Error processing command: {e}")
                    speak("There was an error processing your command.", "Υπήρξε σφάλμα κατά την επεξεργασία της εντολής σου.")
        except KeyboardInterrupt:
            print("Assistant stopped by user.")
            speak("Goodbye.", "Αντίο.")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            speak("An unexpected error occurred.", "Προέκυψε απρόσμενο σφάλμα.")
