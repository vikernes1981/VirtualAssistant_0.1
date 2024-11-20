from globals import current_language
from speech import speak, recognize_speech
from wake_word import listen_for_wake_word
from process_commands import process_command
from database import create_feedback_table

if __name__ == "__main__":
    try:
        # Initialize the feedback table
        create_feedback_table()
    except Exception as e:
        print(f"Error initializing the database: {e}")
        speak("There was an error initializing the database.", "Υπήρξε σφάλμα κατά την αρχικοποίηση της βάσης δεδομένων.")
    
    while True:
        try:
            # Step 1: Listen for the wake word
            listen_for_wake_word("jarvis_linux.ppn")  # Ensure correct path to your wake word model
            
            # Step 2: Greet the user
            speak("Ahoy.", "Γεια σου! Πώς μπορώ να σε βοηθήσω;")
            
            # Step 3: Recognize speech input
            user_input = recognize_speech()
            if user_input:
                # Step 4: Process the user's command
                try:
                    process_command(user_input)
                except Exception as e:
                    print(f"Error processing command: {e}")
                    speak("There was an error processing your command.", 
                          "Υπήρξε σφάλμα κατά την επεξεργασία της εντολής σου.")
        except KeyboardInterrupt:
            print("Assistant stopped by user.")
            speak("Goodbye.", "Αντίο.")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            speak("An unexpected error occurred.", "Προέκυψε απρόσμενο σφάλμα.")
