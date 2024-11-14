from globals import current_language, recognizer  # Import global variables
from speech import speak, recognize_speech
from wake_word import listen_for_wake_word
from database import create_feedback_table
from process_commands import process_command

if __name__ == "__main__":
    create_feedback_table()  # Initialize the database if needed
    while True:  # Keep the assistant running
        listen_for_wake_word("jarvis_linux.ppn")  # Use the wake word file (replace as needed)
        speak("Hello!", "Γεια σου!")  # Greet the user
        user_input = recognize_speech()  # Get user input
        if user_input:
            process_command(user_input)  # Process the user's command
