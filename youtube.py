import os
from yt_dlp import YoutubeDL
import vlc
import time
import webbrowser
from speech import recognize_speech, speak  # Assuming you have these functions for user input and responses
import urllib.parse  # For URL encoding user input

player = None  # Global VLC player instance
music_paused = False  # Global flag to track pause state

def stop_current_music():
    """Stop the currently playing music if there is any."""
    global player
    try:
        if player is not None and player.is_playing():
            player.stop()
            print("Stopped currently playing music.")
    except Exception as e:
        print(f"Error stopping music: {e}")
        speak("An error occurred while trying to stop the music.", "Προέκυψε σφάλμα κατά την προσπάθεια διακοπής της μουσικής.")

def play_youtube_music():
    global player

    try:
        # Stop any music that is already playing
        stop_current_music()

        # Present options to the user
        speak(
            "What would you like to listen to?",
            "Τι θα ήθελες να ακούσεις; Έχεις τρεις επιλογές: Λόφι, Γουόρκραφτ ή να καθορίσεις ένα θέμα μουσικής ή καλλιτέχνη."
        )
        user_choice = recognize_speech()  # Function to capture user input via speech

        # Determine which URL to use based on user choice
        if user_choice:
            user_choice = user_choice.lower()
            if "relax" in user_choice or "χαλαρώσω" in user_choice:  # Check for English ("relax") and Greek ("χαλαρώσω")
                print("Playing Lofi music.")
                video_url = "https://www.youtube.com/watch?v=sF80I-TQiW0"  # Lofi URL
                filename = "lofi_audio.m4a"  # Specify a name for the Lofi file
            elif "warcraft" in user_choice or "γουόρκραφτ" in user_choice:  # Check for English ("warcraft") and Greek ("γουόρκραφτ")
                print("Playing Warcraft music.")
                video_url = "https://www.youtube.com/watch?v=ebmwJnhtMgY"  # Warcraft URL
                filename = "warcraft_audio.m4a"  # Specify a name for the Warcraft file
            else:
                # Construct a YouTube search URL based on user input and open in browser
                query = urllib.parse.quote(user_choice)  # URL encode the user input
                search_url = f"https://www.youtube.com/results?search_query={query}"
                speak(f"Searching YouTube for {user_choice}.", f"Αναζήτηση στο YouTube για {user_choice}.")
                webbrowser.open(search_url)
                return  # Exit the function to avoid further processing

        # Check if the file already exists
        if os.path.exists(filename):
            print(f"File {filename} already exists. Playing the existing file.")
        else:
            # Download/stream the best audio using yt-dlp
            options = {
                'format': 'bestaudio/best',
                'noplaylist': True,
                'quiet': True,
                'outtmpl': filename  # Use specified filename
            }

            with YoutubeDL(options) as ydl:
                try:
                    ydl.extract_info(video_url, download=True)
                    print(f"Downloaded and saved as {filename}")
                except Exception as e:
                    print(f"Error downloading video: {e}")
                    speak("An error occurred while trying to download the music.", "Προέκυψε σφάλμα κατά τη λήψη της μουσικής.")
                    return

        # Use VLC to play audio
        if os.path.exists(filename):
            player = vlc.MediaPlayer(filename)
            player.play()
            time.sleep(1)  # Give some time to start playing
        else:
            print("Error: Audio file not found.")
            speak("An error occurred while trying to play the music.", "Προέκυψε σφάλμα κατά την προσπάθεια αναπαραγωγής της μουσικής.")

    except Exception as e:
        print(f"Unexpected error in play_youtube_music: {e}")
        speak("An unexpected error occurred while trying to play music.", "Προέκυψε απρόσμενο σφάλμα κατά την προσπάθεια αναπαραγωγής της μουσικής.")

def pause_music_vlc():
    global player, music_paused
    try:
        if player is not None:
            if player.is_playing() and not music_paused:
                player.pause()
                music_paused = True
                print("Music paused.")
            elif music_paused:
                player.play()
                music_paused = False
                print("Music resumed.")
    except Exception as e:
        print(f"Error pausing/resuming music: {e}")
        speak("An error occurred while trying to pause or resume the music.", "Προέκυψε σφάλμα κατά την προσπάθεια παύσης ή συνέχισης της μουσικής.")

def stop_music_vlc():
    global player
    try:
        if player is not None:
            player.stop()
            player = None
            print("Music stopped.")
        else:
            print("No music is currently playing.")
    except Exception as e:
        print(f"Error stopping music: {e}")
        speak("An error occurred while trying to stop the music.", "Προέκυψε σφάλμα κατά την προσπάθεια διακοπής της μουσικής.")

def set_vlc_volume(volume_level):
    """Set the volume of VLC player."""
    try:
        if player:
            # Volume level should be between 0 (mute) and 100 (max)
            volume_level = max(0, min(100, volume_level))
            player.audio_set_volume(volume_level)
            print(f"VLC volume set to {volume_level}%")
    except Exception as e:
        print(f"Error setting VLC volume: {e}")
        speak("An error occurred while trying to set the volume.", "Προέκυψε σφάλμα κατά την προσπάθεια ρύθμισης της έντασης.")
