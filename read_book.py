"""
Provides functionality to fetch, list, select, and play audiobooks from a remote API.

Supports voice-based selection and playback resumption using mpv and yt_dlp.
"""

import os
import time
import json
import requests
import subprocess
import yt_dlp
from speech import speak, recognize_speech
from globals import number_map, PLAYBACK_STATE_FILE

API_URL = "https://techodyssey.org/audiobooks"

def fetch_audiobooks_from_api() -> list[dict]:
    try:
        response = requests.get(API_URL, timeout=5)
        if response.status_code == 200:
            return response.json()
        speak("Error fetching audiobooks from the API.")
        print(f"Error: Received status code {response.status_code}")
    except requests.RequestException as e:
        speak("An error occurred while contacting the audiobook service.")
        print(f"Request error: {e}")
    except Exception as e:
        speak("An unexpected error occurred while fetching audiobooks.")
        print(f"Error: {e}")
    return []

def list_audiobooks(audiobooks: list[dict]) -> list[dict] | None:
    if not audiobooks:
        speak("No audiobooks are available at the moment.")
        return None

    speak("Here are the available audiobooks.")
    print("\n\n========== 🎧 AVAILABLE AUDIOBOOKS ==========")
    for idx, book in enumerate(audiobooks):
        print(f"{idx + 1}. {book['title']} by {book['author']}")
    print("=============================================\n\n")
    return audiobooks


def select_audiobook(audiobooks: list[dict]) -> dict | None:
    while True:
        speak("Please say the number of the book you want to listen to. You can also say 'exit' to cancel.")
        print("Please say the number of the book you want to listen to. You can also say 'exit' to cancel.")
        
        user_input = recognize_speech(expected_type="number")
        if user_input:
            print(f"You said: {user_input}")
        else:
            speak("I didn't hear anything.")
            continue

        if "exit" in user_input.lower():
            return "EXIT_FLAG"

        choice_raw = user_input.lower().strip()
        selected = number_map.get(choice_raw)
        if selected and 1 <= selected <= len(audiobooks):
            return audiobooks[selected - 1]

        speak("That doesn't match any book. Try again.")


def play_audio(url: str, title: str) -> None:
    try:
        safe_title = "".join(c if c.isalnum() or c in (" ", "-", "_") else "_" for c in title).strip()
        file_name = f"{safe_title}.webm"

        if not os.path.exists(file_name):
            ydl_opts = {
                'format': 'bestaudio/best',
                'noplaylist': True,
                'outtmpl': file_name,
                'quiet': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(f"Downloaded audio: {file_name}")

        playback_data = {}
        playback_position = 0
        if os.path.exists(PLAYBACK_STATE_FILE):
            with open(PLAYBACK_STATE_FILE, 'r') as f:
                playback_data = json.load(f)
                playback_position = playback_data.get(title, 0)
        if playback_position > 0:
            print(f"[Assistant]: Resume from last position at {playback_position} seconds? (y/n)")
            resume_choice = input(">> ").strip().lower()
            if resume_choice != 'y':
                playback_position = 0
                
        while True:
            print(f"Playing '{title}' from {playback_position} seconds...")
            start_time = time.time()
            process = subprocess.Popen(
                ["mpv", f"--start={playback_position}", file_name],
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            print("[Assistant]: Press 'p' to pause, or 's' to stop.")
            choice = input(">> ").strip().lower()
            process.terminate()
            process.wait()
            elapsed = int(time.time() - start_time)
            playback_position += elapsed

            if choice == 's':
                playback_data[title] = playback_position
                with open(PLAYBACK_STATE_FILE, 'w') as f:
                    json.dump(playback_data, f, indent=4)
                print("Playback stopped.")
                break

            elif choice == 'p':
                print("[Assistant]: Playback paused. Press 'u' to resume or 's' to stop.")
                while True:
                    sub_choice = input(">> ").strip().lower()
                    if sub_choice == 'u':
                        break
                    elif sub_choice == 's':
                        playback_data[title] = playback_position
                        with open(PLAYBACK_STATE_FILE, 'w') as f:
                            json.dump(playback_data, f, indent=4)
                        print("Playback stopped.")
                        return

    except Exception as e:
        speak("There was an error playing the audiobook.")
        print(f"Playback error: {e}")


def select_and_play_audiobook() -> None:
    audiobooks = fetch_audiobooks_from_api()
    listed = list_audiobooks(audiobooks)
    if not listed:
        return

    selected = select_audiobook(listed)
    if selected == "EXIT_FLAG":
        speak("Exiting audiobook selection.")
        return
    if selected:
        title = selected["title"]
        speak(f"Playing {title} by {selected['author']}.")
        play_audio(selected["url"], title)
    else:
        speak("No valid selection was made.")
