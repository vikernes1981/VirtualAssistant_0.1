import os
import speech_recognition as sr
from gtts import gTTS
from globals import current_language, recognizer  # Import global variables
from langdetect import detect
import time

def speak(text_en, text_gr=None):
    """Generate and play speech based on the current language setting."""
    try:
        start_time = time.time()

        lang = 'el' if current_language == 'el' else 'en'  # Switch language based on current setting
        text_to_speak = text_gr if current_language == 'el' else text_en
        tts = gTTS(text=text_to_speak, lang=lang)
        tts.save("response.mp3")

        if os.path.exists("response.mp3"):
            os.system("mpg123 response.mp3")  # Play the generated speech
            print(f"Speak: Operation took {time.time() - start_time:.2f} seconds")
        else:
            print("Error: Could not generate the speech file.")
            raise FileNotFoundError("Generated speech file not found.")
    except Exception as e:
        print(f"Error generating or playing speech: {e}")
        if lang == 'el':
            print("Υπήρξε σφάλμα κατά τη δημιουργία ή την αναπαραγωγή της ομιλίας.")
        else:
            print("There was an error generating or playing the speech.")

def recognize_speech():
    """Recognize speech input and detect the language of the recognized text."""
    global current_language  # Use the global variable to update the language setting
    while True:  # Infinite loop until valid input is recognized
        try:
            with sr.Microphone() as source:
                print("Listening for your input...")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
                try:
                    text = recognizer.recognize_google(audio, language="el-GR").lower()
                    print(f"You said: {text}")

                    # Detect the language of the recognized text and adjust `current_language`
                    detected_language = detect(text)
                    if detected_language == 'el':
                        current_language = 'el'  # Set to Greek if Greek is detected
                    else:
                        current_language = 'en'  # Set to English if English is detected

                    return text.lower()  # Convert text to lowercase for easier command matching
                except sr.UnknownValueError:
                    print("Sorry, I could not understand the audio. Please try again.")
                    speak("I did not understand what you said. Please try again.", "Δεν κατάλαβα τι είπες. Παρακαλώ προσπάθησε ξανά.")
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
                    speak("There was a problem with the speech recognition service.", "Υπήρξε πρόβλημα με την υπηρεσία αναγνώρισης ομιλίας.")
                    return None
        except sr.RequestError as mic_error:
            print(f"Microphone error: {mic_error}")
            speak("There was a problem with accessing the microphone.", "Υπήρξε πρόβλημα με την πρόσβαση στο μικρόφωνο.")
            return None
        except Exception as e:
            print(f"Unexpected error during speech recognition: {e}")
            speak("An unexpected error occurred while trying to recognize speech.", "Προέκυψε απρόσμενο σφάλμα κατά την αναγνώριση ομιλίας.")
            return None
