import threading
import time
from speech import speak, recognize_speech, record_audio, transcribe_with_whisper, print_listening_countdown
from database import insert_dictated_text
from wit_integration import get_intent_from_wit

# Shared state
stop_flag = False
dictation_text = ""
dictation_lock = threading.Lock()
DICTATION_FILE = "dictation.txt"
STOP_PHRASES = ["stop dictation", "end dictation", "cancel dictation"]

def detect_stop_phrase_in_file(poll_interval: float = 1.0) -> None:
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
                if any(phrase in line.lower() for phrase in STOP_PHRASES):
                    print("Stop phrase detected in file.")
                    stop_flag = True
                    return
        except FileNotFoundError:
            pass
        time.sleep(poll_interval)

def real_time_dictation() -> str:
    global stop_flag, dictation_text
    stop_flag = False
    dictation_text = ""
    RECORD_BLOCK_DURATION = 20  # Keeping your preferred chunk size

    with open(DICTATION_FILE, "w") as f:
        f.write("")

    speak("I'm ready. Say 'stop dictation' to end.")
    print("Start dictating. You can also say 'delete words'.")
    threading.Thread(target=detect_stop_phrase_in_file, daemon=True).start()

    try:
        while not stop_flag:
            audio_path = record_audio(duration=RECORD_BLOCK_DURATION)
            print("Still listening... say 'stop dictation' to finish.")
            if not audio_path:
                speak("There was an issue recording.")
                break

            transcription = transcribe_with_whisper(audio_path, language="en").strip().lower()
            if not transcription:
                continue

            # Detect and remove all stop phrases from anywhere in the transcription
            for phrase in STOP_PHRASES:
                if phrase in transcription:
                    print(f"[!] Stop phrase '{phrase}' detected — trimming transcription.")
                    transcription = transcription.split(phrase)[0].strip()
                    stop_flag = True
                    break


            print("You said:", transcription)

            with open(DICTATION_FILE, "a") as f:
                f.write(transcription + "\n")

            intent = get_intent_from_wit(transcription)
            if intent == "delete_text":
                speak("How many words should I delete?")
                response = recognize_speech(expected_type="number")
                try:
                    num_words = int(response) if response and response.isdigit() else 0
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

            # Add punctuation and spacing
            if not transcription.endswith("."):
                transcription += "."
            with dictation_lock:
                dictation_text += transcription.strip().capitalize() + " "

    except Exception as e:
        print(f"Dictation error: {e}")
        speak("An error occurred during dictation.")
        return ""

    final_text = dictation_text.strip()
    print("\n" + "-" * 50)
    print("Final Dictated Text:", final_text)
    print("Dictation result:", final_text)
    print("-" * 50 + "\n")

    if final_text:
        try:
            if insert_dictated_text(final_text, language="en"):
                speak("The text has been saved.")
            else:
                speak("Failed to save the text.")
        except Exception as e:
            print(f"Database error: {e}")
            speak("There was an error saving the text.")

    return final_text

