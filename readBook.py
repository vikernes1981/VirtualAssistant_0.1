import os
import requests
import vlc
import yt_dlp
import time
from youtubesearchpython import VideosSearch
from speech import speak  # Assuming this is your TTS function

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

def play_audio(url):
    try:
        temp_file = 'temp_audio.mp3'  # Set expected output file

        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'outtmpl': temp_file,  # Save as 'temp_audio.mp3'
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'postprocessor_args': ['-y'],  # Overwrite existing files if needed
            'nopostoverwrites': False  # Ensure it doesn't keep webm file
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Check if the file was created
        if os.path.exists(temp_file):
            print(f"Audio file '{temp_file}' downloaded successfully.")
        else:
            print("Audio file not found.")
            return

        # Small delay before playback to ensure the file is ready
        time.sleep(2)

        # Initialize VLC player to play audio
        player = vlc.MediaPlayer(f"file://{os.path.abspath(temp_file)}")
        print("Playing audiobook...")
        player.play()

        # Wait for playback to start
        time.sleep(1)

        # Monitor playback or wait for user input to stop
        input("Press Enter to stop playback...\n")
        player.stop()

        # Clean up temporary file
        os.remove(temp_file)
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
        speak(f"Playing {selected_audiobook['title']} by {selected_audiobook['author']}.", f"Αναπαραγωγή του {selected_audiobook['title']} από τον {selected_audiobook['author']}.")
        print(f"Playing: {selected_audiobook['title']} by {selected_audiobook['author']}")
        play_audio(selected_audiobook['url'])
    else:
        speak("No valid selection was made.", "Δεν έγινε έγκυρη επιλογή.")

# Example usage
select_and_play_audiobook()
