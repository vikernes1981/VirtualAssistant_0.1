"""
Handles real-time voice dictation using Whisper transcription and live file monitoring.

Dictation stops automatically when "stop dictation" is detected in the transcribed file,
and supports deleting words mid-dictation via a Wit.ai intent.
"""

import threading
import time
from speech import speak, recognize_speech, record_audio, transcribe_with_whisper
from database import insert_dictated_text
from wit_integration import get_intent_from_wit

# Shared state
stop_flag = False
dictation_text = ""
dictation_lock = threading.Lock()
DICTATION_FILE = "dictation.txt"  # Temp file to monitor live transcription


def detect_stop_phrase_in_file(stop_phrase: str = "stop dictation", poll_interval: float = 1.0) -> None:
    """
    Monitor the transcription output file for a stop phrase.

    Args:
        stop_phrase (str): Phrase that signals end of dictation.
        poll_interval (float): Time between polling the file in seconds.
    """
    global stop_flag
    print("Watching file for stop command...")
    last_position = 0

    while not stop_flag:
        try:
            with open(DICTATION_FILE, "r") as f:
                f.seek(last_position)
                new_lines = f.readlines()
                last_position = f.tell()

            for line in new_lines:
                if stop_phrase in line.lower():
                    print("Stop word detected in file.")
                    stop_flag = True
                    return

        except FileNotFoundError:
            pass  # File may not exist yet

        time.sleep(poll_interval)


def real_time_dictation(stop_phrase: str = "stop dictation") -> str:
    """
    Perform continuous dictation using Whisper and file monitoring.
    Allows deleting words with a voice command, and stops on a spoken stop phrase.

    Args:
        stop_phrase (str): Spoken phrase that ends dictation.

    Returns:
        str: Final transcribed and optionally edited text.
    """
    global stop_flag, dictation_text
    stop_flag = False
    dictation_text = ""

    # Reset output file
    with open(DICTATION_FILE, "w") as f:
        f.write("")

    speak("I'm ready. Say 'stop dictation' to end.")
    print("Start dictating. You can also say 'delete words'.")

    # Start file-monitoring thread
    threading.Thread(target=detect_stop_phrase_in_file, daemon=True).start()

    try:
        while not stop_flag:
            audio_path = record_audio(duration=20)
            if not audio_path:
                speak("There was an issue recording.")
                break

            transcription = transcribe_with_whisper(audio_path).strip().lower()
            if not transcription:
                continue

            print("You said:", transcription)

            # Append to monitoring file
            with open(DICTATION_FILE, "a") as f:
                f.write(transcription + "\n")

            # Check for deletion intent
            intent = get_intent_from_wit(transcription)
            if intent == "delete_text":
                speak("How many words should I delete?")
                response = recognize_speech(expected_type="number")
                try:
                    if response and response.isdigit():
                        num_words = int(response)
                    else:
                        num_words = 0

                    with dictation_lock:
                        words = dictation_text.strip().split()
                        if num_words > 0 and len(words) >= num_words:
                            dictation_text = " ".join(words[:-num_words])
                            speak(f"Deleted the last {num_words} words.")
                        else:
                            speak("Not enough words to delete.")
                except Exception as e:
                    print(f"[✗] Error deleting words: {e}")
                    speak("Something went wrong.")
                continue

            # Append transcribed sentence to memory buffer
            with dictation_lock:
                dictation_text += transcription + " "

    except Exception as e:
        print(f"Dictation error: {e}")
        speak("An error occurred during dictation.")
        return ""

    # Final save
    if dictation_text.strip():
        try:
            if insert_dictated_text(dictation_text.strip(), language="en"):
                speak("The text has been saved.")
            else:
                speak("Failed to save the text.")
        except Exception as e:
            print(f"Database error: {e}")
            speak("There was an error saving the text.")

    return dictation_text.strip()
