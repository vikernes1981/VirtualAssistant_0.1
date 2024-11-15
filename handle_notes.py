from speech import recognize_speech, speak
from database import insert_note, get_all_notes, delete_note_by_id



# This function handles note-taking interactions
def handle_notes():
    while True:
        speak("Would you like to add or view a note?", 
              "Θα ήθελες να προσθέσεις μια νέα σημείωση ή να δεις υπάρχουσες σημειώσεις;")
        user_input = recognize_speech()

        if not user_input:
            continue

        if "create a note" in user_input or "προσθέτω" in user_input:
            while True:
                speak("Please say the note you would like to add.", "Παρακαλώ πες τη σημείωση που θέλεις να προσθέσεις.")
                note_content = recognize_speech()
                if note_content:
                    success = insert_note(note_content)
                    if success:
                        speak("Note added successfully.", "Η σημείωση προστέθηκε με επιτυχία.")
                    else:
                        speak("There was an error adding the note.", "Υπήρξε σφάλμα κατά την προσθήκη της σημείωσης.")
                    
                    speak("Would you like to add another note?", "Θέλεις να προσθέσεις άλλη μια σημείωση;")
                    response = recognize_speech()
                    print(f"Recognized response: {response}")  # Debugging statement
                    if "no" in response or "όχι" in response:
                        break

        elif "view my notes" in user_input or "βλέπω" in user_input:
            notes = get_all_notes()
            if notes:
                speak("Here are your notes.", "Εδώ είναι οι σημειώσεις σου.")
                for note in notes:
                    print(f"Note {note[0]}: {note[1]}")  # Debugging statement
            else:
                speak("You have no notes.", "Δεν έχεις σημειώσεις.")

        else:
            speak("I did not understand your request. Please say add, view, or delete.", 
                  "Δεν κατάλαβα το αίτημά σου. Παρακαλώ πες προσθέτω, βλέπω ή διαγράφω.")
        
        speak("Would you like to continue with notes?", "Θέλεις να συνεχίσεις με τις σημειώσεις;")
        response = recognize_speech()
        if response is None:
            speak("I did not hear anything. Please try again.", "Δεν άκουσα τίποτα. Παρακαλώ προσπάθησε ξανά.")
            continue  # This will prompt the user again if no response is captured

        response = response.lower()  # Convert to lowercase for consistent comparison
        print(f"Recognized response: {response}")  # Debugging statement

        if "no" in response or "όχι" in response:
            print("Exiting notes loop")  # Debugging statement
            break  # Exit the loop if the user says "no" or "όχι"



