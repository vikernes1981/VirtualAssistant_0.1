"""
Handles all speech-related operations including TTS, STT (Google + Whisper),
audio recording, and basic speech validation.
"""

import subprocess
import requests
import numpy as np
import sounddevice as sd
import speech_recognition as sr
from scipy.io.wavfile import write
from gtts import gTTS
from dotenv import load_dotenv
from globals import number_map
import os

# Optional fallback pause (only imported if available)
try:
    from youtube import pause_music_vlc
except ImportError:
    pause_music_vlc = lambda: None

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("Missing OpenAI API key.")

recognizer = sr.Recognizer()


def speak(text: str) -> None:
    """
    Convert text to speech using Google TTS and play it via mpg123.

    Args:
        text (str): The sentence to vocalize.
    """
    try:
        tts = gTTS(text=text, lang="en")
        tts.save("response.mp3")
        subprocess.run(["mpg123", "response.mp3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Error in speak(): {e}")


def record_audio(filename: str = "fallback_audio.wav", duration: int = 5, fs: int = 44100) -> str | None:
    """
    Record audio from the microphone for a fixed duration.

    Args:
        filename (str): Where to save the recorded WAV file.
        duration (int): How long to record in seconds.
        fs (int): Sampling rate in Hz.

    Returns:
        str or None: Path to the recorded file or None on failure.
    """
    try:
        print(f"Recording for {duration} seconds...")
        audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="int16")
        sd.wait()
        write(filename, fs, audio_data)
        return filename
    except Exception as e:
        print(f"Error recording audio: {e}")
        return None


def transcribe_with_whisper(audio_path: str) -> str:
    """
    Transcribe audio using OpenAI Whisper API.

    Args:
        audio_path (str): Path to the audio file to transcribe.

    Returns:
        str: Transcribed text or empty string on error.
    """
    try:
        with open(audio_path, "rb") as audio_file:
            response = requests.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {openai_api_key}"},
                files={"file": audio_file},
                data={"model": "whisper-1"}
            )
        return response.json().get("text", "")
    except Exception as e:
        print(f"Whisper API error: {e}")
        return ""


def recognize_speech(expected_type: str | None = None) -> str | None:
    """
    Record speech and try to transcribe it with Google STT first, then Whisper if needed.

    Args:
        expected_type (str | None): Optional hint for validating output ("number", etc.)

    Returns:
        str or None: Transcribed and optionally validated result.
    """
    try:
        audio_file = record_audio()
        if not audio_file:
            speak("I could not record any audio.")
            return None

        try:
            with sr.AudioFile(audio_file) as source:
                audio = recognizer.record(source)
            text = recognizer.recognize_google(audio).strip().lower()
            print(f"Google Transcription: {text}")
            return validate_transcription(text, expected_type)
        except (sr.UnknownValueError, sr.RequestError):
            print("Google STT failed, falling back to Whisper.")

        text = transcribe_with_whisper(audio_file).strip().lower()
        print(f"Whisper Transcription: {text}")
        return validate_transcription(text, expected_type)

    except Exception as e:
        print(f"Transcription error: {e}")
        speak("An error occurred during voice processing.")
        return None


def validate_transcription(text: str, expected_type: str | None) -> str | None:
    """
    Post-process transcription result based on expected type.

    Args:
        text (str): The raw transcribed text.
        expected_type (str | None): If "number", tries to normalize spoken numerals.

    Returns:
        str or None: Cleaned value or None if validation fails.
    """
    if expected_type == "number":
        if text.isdigit():
            return text
        return str(number_map.get(text)) if text in number_map else None
    return text
