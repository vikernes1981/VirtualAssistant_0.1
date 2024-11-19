import speech_recognition as sr
from speech import speak  # Importing the speak function
from globals import current_language, recognizer  # Importing global variables from globals.py
from database import insert_dictated_text  # Importing the database function

def real_time_dictation(stop_word="τέλος"):
    global current_language
    global recognizer

    try:
        speak("I am ready to start dictation.", "Είμαι έτοιμος να αρχίσω την υπαγόρευση. Πες 'τέλος' για να σταματήσεις.")
        with sr.Microphone() as source:
            try:
                speak("Please wait while I adjust to the background noise.", "Παρακαλώ περίμενε, ρυθμίζω τον θόρυβο του περιβάλλοντος.")
                recognizer.adjust_for_ambient_noise(source, duration=3)
                print("Noise adjustment complete. Start speaking. Say 'τέλος' to stop or 'delete last' to remove the last word.")
            except Exception as e:
                print(f"Error during noise adjustment: {e}")
                speak("There was an error adjusting to the background noise.", "Υπήρξε σφάλμα κατά την προσαρμογή στον θόρυβο του περιβάλλοντος.")
                return ""

            text_output = ""

            try:
                while True:
                    try:
                        audio = recognizer.listen(source, timeout=40, phrase_time_limit=60)
                        try:
                            text = recognizer.recognize_google(audio, language="el-GR").lower()
                            if stop_word in text:
                                speak("Dictation stopped.", "Η υπαγόρευση σταμάτησε.")
                                print("\nDictation stopped.")
                                break
                            elif "delete last" in text or "διαγραφή τελευταίου" in text:
                                words = text_output.strip().split()
                                if words:
                                    removed_word = words.pop()
                                    text_output = " ".join(words)
                                    print(f"The last word '{removed_word}' has been removed.")
                                    print(f"Updated text: {text_output}")
                                else:
                                    speak("There is no word to remove.", "Δεν υπάρχει λέξη για διαγραφή.")
                            else:
                                text_output += text + " "
                                print(text, end=" ", flush=True)
                        except sr.UnknownValueError:
                            print("\nCould not understand audio, please try again...")
                        except sr.RequestError as e:
                            print(f"\nThere was an issue with the speech recognition service: {e}")
                            speak("There was an issue with the speech recognition service.", "Υπήρξε πρόβλημα με την υπηρεσία αναγνώρισης ομιλίας.")
                            break
                    except sr.WaitTimeoutError:
                        print("\nTimeout waiting for speech input.")
                        speak("I did not hear anything. Please try again.", "Δεν άκουσα τίποτα. Παρακαλώ προσπάθησε ξανά.")
                        continue
                    except KeyboardInterrupt:
                        print("\nDictation stopped by keyboard interruption.")
                        break
            except Exception as e:
                print(f"Unexpected error during dictation: {e}")
                speak("An unexpected error occurred during dictation.", "Προέκυψε απρόσμενο σφάλμα κατά την υπαγόρευση.")
    except Exception as e:
        print(f"Error initializing dictation: {e}")
        speak("An error occurred while starting dictation.", "Υπήρξε σφάλμα κατά την έναρξη της υπαγόρευσης.")
        return ""

    # Save text to the database if there is any
    if text_output.strip():
        language = 'gr' if current_language == 'gr' else 'en'
        try:
            if insert_dictated_text(text_output.strip(), language):
                speak("The text has been stored in the database.", "Το κείμενο αποθηκεύτηκε στη βάση δεδομένων.")
            else:
                speak("There was an error saving the text to the database.", "Υπήρξε σφάλμα κατά την αποθήκευση του κειμένου στη βάση δεδομένων.")
        except Exception as e:
            print(f"Error saving text to the database: {e}")
            speak("There was an error while saving the text.", "Υπήρξε σφάλμα κατά την αποθήκευση του κειμένου.")

    return text_output
