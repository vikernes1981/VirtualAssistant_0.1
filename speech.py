import os
import sounddevice as sd
from scipy.io.wavfile import write
import requests
import speech_recognition as sr
from gtts import gTTS
from globals import current_language
from langdetect import detect
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please ensure it's set in the .env file.")

# Initialize Recognizer
recognizer = sr.Recognizer()

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

def record_audio(filename="fallback_audio.wav", duration=5, fs=44100):
    """
    Records audio from the microphone and saves it as a WAV file.
    Args:
        filename: Name of the file to save the audio.
        duration: Duration of the recording in seconds.
        fs: Sampling frequency (default is 44100 Hz).
    Returns:
        str: The file path of the recorded audio.
    """
    try:
        print(f"Recording for {duration} seconds...")
        audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="int16")
        sd.wait()  # Wait until the recording is finished
        write(filename, fs, audio_data)  # Save as WAV file
        print(f"Audio recorded and saved to {filename}")
        return filename
    except Exception as e:
        print(f"Error recording audio: {e}")
        return None

def transcribe_with_whisper(audio_path):
    """
    Sends audio to Whisper API for transcription.
    Args:
        audio_path: The path to the audio file.
    Returns:
        str: Transcribed text.
    """
    try:
        with open(audio_path, "rb") as audio_file:
            response = requests.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {openai_api_key}"},
                files={"file": audio_file},
                data={"model": "whisper-1"}
            )
        result = response.json()
        return result.get("text", "")
    except Exception as e:
        print(f"Error using Whisper API: {e}")
        return ""

# Number mapping dictionary for numeric recognition
number_map = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "1": 1, "2": 2, "3": 3, "4": 4, "5": 5,
    "6": 6, "7": 7, "8": 8, "9": 9, "10": 10
}

def recognize_speech(expected_type=None):
    """
    Recognize speech input with Google Speech-to-Text first, and fallback to Whisper.
    Args:
        expected_type (str): The type of expected input ("number", "text", etc.).
    Returns:
        str: The recognized text or None if both methods fail.
    """
    try:
        # Record audio
        audio_file = record_audio(filename="fallback_audio.wav", duration=5)
        if not audio_file:
            speak("I could not record any audio. Please try again.", "Δεν μπόρεσα να καταγράψω ήχο. Παρακαλώ προσπάθησε ξανά.")
            return None

        # Step 1: Try Google Speech-to-Text
        try:
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_file) as source:
                audio = recognizer.record(source)
            transcription = recognizer.recognize_google(audio).strip().lower()
            print(f"Google Transcription: {transcription}")
            return validate_transcription(transcription, expected_type)
        except sr.UnknownValueError:
            print("Google Speech-to-Text couldn't understand the audio.")
        except sr.RequestError as e:
            print(f"Google Speech-to-Text failed with error: {e}")

        # Step 2: Fallback to Whisper
        print("Trying Whisper for transcription...")
        transcription = transcribe_with_whisper(audio_file).strip().lower()
        print(f"Whisper Transcription: {transcription}")
        return validate_transcription(transcription, expected_type)
    except Exception as e:
        print(f"Unexpected error during transcription: {e}")
        speak("An unexpected error occurred while processing your audio.", 
              "Προέκυψε απρόσμενο σφάλμα κατά την επεξεργασία του ήχου σου.")
        return None


def validate_transcription(transcription, expected_type):
    """
    Validate the transcription based on the expected type.
    Args:
        transcription (str): The transcribed text.
        expected_type (str): The expected type of input ("number", "text").
    Returns:
        str: The validated transcription or None if invalid.
    """
    if expected_type == "number":
        if transcription.isdigit():
            return transcription
        elif transcription in number_map:
            return str(number_map[transcription])
        else:
            print(f"Invalid number: {transcription}")
            return None
    return transcription  # For general text inputs
