import speech_recognition as sr
from speech import speak  # Importing the speak function
from globals import current_language, recognizer  # Importing global variables from globals.py
from database import insert_dictated_text  # Importing the database function

def real_time_dictation(stop_word="τέλος"):
    global current_language
    global recognizer

    speak("I am ready to start dictation.", "Είμαι έτοιμος να αρχίσω την υπαγόρευση. Πες 'τέλος' για να σταματήσεις.")
    with sr.Microphone() as source:
        speak("Please wait while I adjust to the background noise.", "Παρακαλώ περίμενε, ρυθμίζω τον θόρυβο του περιβάλλοντος.")
        recognizer.adjust_for_ambient_noise(source, duration=3)
        print("Noise adjustment complete. Start speaking. Say 'τέλος' to stop or 'delete last' to remove the last word.")

        text_output = ""

        try:
            while True:
                audio = recognizer.listen(source, timeout=40, phrase_time_limit=60)
                try:
                    text = recognizer.recognize_google(audio, language="el-GR").lower()
                    if stop_word in text:
                        speak("Dictation stopped.", "Η υπαγόρευση σταμάτησε.")
                        print("\nDictation stopped.")
                        break
                    elif "delete last" in text or "διαγραφή τελευταίου" in text:
                        # Remove the last word from text_output
                        words = text_output.strip().split()
                        if words:
                            removed_word = words.pop()  # Remove the last word
                            text_output = " ".join(words)
                            print(f"The last word '{removed_word}' has been removed.", "Η τελευταία λέξη αφαιρέθηκε.")
                            print(f"Updated text: {text_output}")  # Show the updated text
                        else:
                            speak("There is no word to remove.", "Δεν υπάρχει λέξη για διαγραφή.")
                    else:
                        text_output += text + " "
                        print(text, end=" ", flush=True)
                except sr.UnknownValueError:
                    print("\nCould not understand audio, please try again...")
                except sr.RequestError as e:
                    print(f"\nThere was an issue with the speech recognition service: {e}")
                    break
        except KeyboardInterrupt:
            print("\nDictation stopped by keyboard interruption.")

    # Save text to the database if there is any
    if text_output.strip():
        language = 'gr' if current_language == 'gr' else 'en'
        if insert_dictated_text(text_output.strip(), language):
            speak("The text has been stored in the database.", "Το κείμενο αποθηκεύτηκε στη βάση δεδομένων.")
        else:
            speak("There was an error saving the text to the database.", "Υπήρξε σφάλμα κατά την αποθήκευση του κειμένου στη βάση δεδομένων.")

    return text_output
