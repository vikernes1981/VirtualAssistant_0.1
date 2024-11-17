import os
import speech_recognition as sr
from gtts import gTTS
from globals import current_language, recognizer  # Import global variables
from langdetect import detect

def speak(text_en, text_gr=None):
    # Generate speech
    lang = 'el' if current_language == 'el' else 'en'  # Switch language based on current setting
    tts = gTTS(text=text_gr if current_language == 'el' else text_en, lang=lang)
    tts.save("response.mp3")
    os.system("mpg123 response.mp3")  # Play the generated speech
    # Resume music after speaking

def recognize_speech():
    global current_language  # Use the global variable to update the language setting
    with sr.Microphone() as source:
        print("Listening for your input...")
        try:
            audio = recognizer.listen(source, timeout=40, phrase_time_limit=60)
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
            print("Sorry, I could not understand the audio.")
            speak("I did not understand what you said.", "Δεν κατάλαβα τι είπες.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            speak("There was a problem with the speech recognition service.", "Υπήρξε πρόβλημα με την υπηρεσία αναγνώρισης ομιλίας.")
            return None
