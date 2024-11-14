import os
import speech_recognition as sr
from gtts import gTTS
from globals import current_language, recognizer  # Import global variables
from langdetect import detect

def speak(text_en, text_gr=None):
    # Generate speech
    lang = 'el' if current_language == 'gr' else 'en'  # Switch language based on current setting
    tts = gTTS(text=text_gr if current_language == 'gr' else text_en, lang=lang)
    tts.save("response.mp3")
    os.system("mpg123 response.mp3")  # Play the generated speech
    # Resume music after speaking

def recognize_speech():
    global current_language  # Use the global variable to update the language setting
    with sr.Microphone() as source:
        print("Listening for your input...")
        try:
            audio = recognizer.listen(source)
            lang = "el-GR" if current_language == 'gr' else "en-US"
            text = recognizer.recognize_google(audio, language=lang)  
            print(f"You said: {text}")
            
            # Detect the language of the recognized text
            detected_language = detect(text)
            if detected_language == 'el':
                current_language = 'gr'  # Switch to Greek if detected language is Greek
            else:
                current_language = 'en'  # Switch to English if detected language is not Greek

            return text.lower()  # Convert text to lowercase for easier command matching
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            speak("I did not understand what you said.", "Δεν κατάλαβα τι είπες.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            speak("There was a problem with the speech recognition service.", "Υπήρξε πρόβλημα με την υπηρεσία αναγνώρισης ομιλίας.")
            return None
