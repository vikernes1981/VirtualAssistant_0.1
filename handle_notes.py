from speech import recognize_speech, speak
from database import insert_note, get_all_notes, delete_note_by_id

def handle_notes():
    while True:
        try:
            speak("Would you like to add, view, or delete a note?", 
                  "Θα ήθελες να προσθέσεις, δεις ή διαγράψεις μια σημείωση;")
            user_input = recognize_speech()

            if not user_input:
                continue

            if "create a note" in user_input or "προσθέτω" in user_input:
                while True:
                    try:
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
                            if response and ("no" in response or "όχι" in response):
                                break
                    except Exception as e:
                        print(f"Error adding note: {e}")
                        speak("There was an error while adding the note.", "Υπήρξε σφάλμα κατά την προσθήκη της σημείωσης.")
                        break

            elif "view my notes" in user_input or "βλέπω" in user_input:
                try:
                    notes = get_all_notes()
                    if notes:
                        speak("Here are your notes.", "Εδώ είναι οι σημειώσεις σου.")
                        for idx, note in enumerate(notes, start=1):
                            print(f"Note {idx}: {note[1]}")
                            speak(f"Note {idx}: {note[1]}", f"Σημείωση {idx}: {note[1]}")
                    else:
                        speak("You have no notes.", "Δεν έχεις σημειώσεις.")
                except Exception as e:
                    print(f"Error retrieving notes: {e}")
                    speak("There was an error retrieving your notes.", "Υπήρξε σφάλμα κατά την ανάκτηση των σημειώσεών σου.")

            elif "delete" in user_input or "διαγράφω" in user_input:
                try:
                    notes = get_all_notes()
                    if notes:
                        speak("Here are your notes.", "Εδώ είναι οι σημειώσεις σου.")
                        for idx, note in enumerate(notes, start=1):
                            print(f"Note {idx}: {note[1]}")

                        speak("Please say the number of the note you want to delete.", 
                              "Παρακαλώ πες τον αριθμό της σημείωσης που θέλεις να διαγράψεις.")
                        response = recognize_speech()
                        number_map = {
                            "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
                            "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15
                        }

                        if response and response in number_map:
                            note_index = number_map[response]
                            if 1 <= note_index <= len(notes):
                                note_id_to_delete = notes[note_index - 1][0]
                                delete_success = delete_note_by_id(note_id_to_delete)
                                if delete_success:
                                    speak("Note deleted successfully.", "Η σημείωση διαγράφηκε με επιτυχία.")
                                else:
                                    speak("There was an error deleting the note.", "Υπήρξε σφάλμα κατά τη διαγραφή της σημείωσης.")
                            else:
                                speak("Invalid note number.", "Μη έγκυρος αριθμός σημείωσης.")
                        else:
                            speak("I did not understand the number. Please try again.", "Δεν κατάλαβα τον αριθμό. Παρακαλώ προσπάθησε ξανά.")
                    else:
                        speak("You have no notes to delete.", "Δεν έχεις σημειώσεις για διαγραφή.")
                except Exception as e:
                    print(f"Error deleting note: {e}")
                    speak("There was an error while trying to delete a note.", "Υπήρξε σφάλμα κατά τη διαγραφή της σημείωσης.")

            else:
                speak("I did not understand your request. Please say add, view, or delete.", 
                      "Δεν κατάλαβα το αίτημά σου. Παρακαλώ πες προσθέτω, βλέπω ή διαγράφω.")
            
            speak("Would you like to continue with notes?", "Θέλεις να συνεχίσεις με τις σημειώσεις;")
            response = recognize_speech()
            if response is None:
                speak("I did not hear anything. Please try again.", "Δεν άκουσα τίποτα. Παρακαλώ προσπάθησε ξανά.")
                continue

            response = response.lower()
            if "no" in response or "όχι" in response:
                break  # Exit the loop if the user says "no" or "όχι"

        except Exception as e:
            print(f"Unexpected error: {e}")
            speak("An unexpected error occurred.", "Προέκυψε απρόσμενο σφάλμα.")
