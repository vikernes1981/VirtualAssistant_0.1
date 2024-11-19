import os
import requests
import yt_dlp
import time
from speech import speak  # Assuming this is your TTS function
import subprocess
import json

API_URL = "https://techodyssey.org/audiobooks"

def fetch_audiobooks_from_api():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            speak("Error fetching audiobooks from the API.", "Σφάλμα κατά την ανάκτηση ακουστικών βιβλίων από την API.")
            print(f"Error: Received status code {response.status_code}")
            return []
    except Exception as e:
        speak("An error occurred while fetching audiobooks from the API.", "Προέκυψε σφάλμα κατά την ανάκτηση ακουστικών βιβλίων από την API.")
        print(f"Error: {e}")
        return []

def list_audiobooks(audiobooks):
    if not audiobooks:
        speak("No audiobooks are available at the moment.", "Δεν υπάρχουν διαθέσιμα ακουστικά βιβλία αυτήν τη στιγμή.")
        print("No audiobooks found.")
        return None
    speak("Here are the available audiobooks.", "Ακολουθούν τα διαθέσιμα ακουστικά βιβλία.")
    print("Available Audiobooks:")
    for idx, book in enumerate(audiobooks):
        print(f"{idx + 1}. {book['title']} by {book['author']}")
    return audiobooks

def select_audiobook(audiobooks):
    try:
        choice = int(input("Select a book by entering its number: ")) - 1
        if 0 <= choice < len(audiobooks):
            return audiobooks[choice]
        else:
            speak("Invalid choice. Please select a valid number.", "Μη έγκυρη επιλογή. Παρακαλώ επιλέξτε έναν έγκυρο αριθμό.")
            print("Invalid choice.")
            return None
    except ValueError:
        speak("Please enter a valid number.", "Παρακαλώ εισάγετε έναν έγκυρο αριθμό.")
        print("Invalid input.")
        return None


def play_audio(url, title):
    try:
        # Sanitize the title for filename use (remove or replace invalid characters)
        safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in title).strip()
        file_name = f"{safe_title}.webm"

        # Check if the file already exists
        if os.path.exists(file_name):
            print(f"'{file_name}' already exists. Skipping download.")
        else:
            # Download audio using yt_dlp
            ydl_opts = {
                'format': 'bestaudio/best',
                'noplaylist': True,
                'outtmpl': file_name,  # Save with book title as filename
                'postprocessors': []  # No post-processing needed for direct webm usage
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # Check if the expected file was created
            if os.path.exists(file_name):
                print(f"Audio file '{file_name}' downloaded successfully.")
            else:
                print("Audio file not found.")
                return
        # Save the playback position to a JSON file
        playback_data = {}
        json_file = "playback_positions.json"
        # Load playback position from JSON file if it exists
        playback_position = 0
        json_file = "playback_positions.json"
        if os.path.exists(json_file):
            with open(json_file, 'r') as f:
                playback_data = json.load(f)
                playback_position = playback_data.get(title, 0)

        while True:
            # Play the audio file with mpv
            print(f"Playing audiobook '{title}' using mpv from position {playback_position} seconds...")
            start_time = time.time()  # Record the start time
            process = subprocess.Popen(
            ["mpv", "--start=" + str(playback_position), file_name],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
            )

            input("Press Enter to stop playback...\n")
            process.terminate()  # Stop playback
            process.wait()  # Ensure process is fully terminated

            # Calculate the elapsed time and update playback position
            elapsed_time = time.time() - start_time
            playback_position += int(elapsed_time)

            # Ask user if they want to resume
            resume = input("Do you want to resume playback? (y/n): ").strip().lower()
            if resume != 'y':
                
                # Load existing playback positions if the file exists
                if os.path.exists(json_file):
                    with open(json_file, 'r') as f:
                        playback_data = json.load(f)

                # Update the playback position for the current book
                playback_data[title] = playback_position

                # Save the updated playback positions back to the file
                with open(json_file, 'w') as f:
                    json.dump(playback_data, f, indent=4)
                break

                
    except Exception as e:
        speak("There was an error fetching or playing the audio.", "Υπήρξε σφάλμα κατά την ανάκτηση ή αναπαραγωγή του ήχου.")
        print(f"Error during playback: {e}")


def select_and_play_audiobook():
    audiobooks = fetch_audiobooks_from_api()
    listed_audiobooks = list_audiobooks(audiobooks)
    if not listed_audiobooks:
        return

    selected_audiobook = select_audiobook(listed_audiobooks)
    if selected_audiobook:
        title = selected_audiobook['title']
        url = selected_audiobook['url']
        speak(f"Playing {title} by {selected_audiobook['author']}.", f"Αναπαραγωγή του {title} από τον {selected_audiobook['author']}.")
        print(f"Playing: {title} by {selected_audiobook['author']}")
        play_audio(url, title)
    else:
        speak("No valid selection was made.", "Δεν έγινε έγκυρη επιλογή.")


# Example usage
select_and_play_audiobook()
