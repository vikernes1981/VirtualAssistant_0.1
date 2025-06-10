"""
Handles YouTube music playback using voice commands and VLC player.

Includes logic for playing, pausing, stopping music, and setting volume.
"""

import os
import time
import json
import vlc
import urllib.parse
import webbrowser
from yt_dlp import YoutubeDL
from speech import recognize_speech, speak
from globals import YOUTUBE_PRESETS

# Global VLC player state
player: vlc.MediaPlayer | None = None
music_paused: bool = False


def stop_current_music() -> None:
    """
    Stop the currently playing VLC track, if any.
    """
    global player
    try:
        if player and player.is_playing():
            player.stop()
            print("Stopped currently playing music.")
    except Exception as e:
        print(f"Error stopping music: {e}")
        speak("An error occurred while trying to stop the music.")


def play_youtube_music() -> None:
    """
    Prompt user for a music preference, attempt to match or search,
    then download (if needed) and play via VLC.
    """
    global player

    try:
        stop_current_music()
        speak("What would you like to listen to?")
        user_choice = recognize_speech()

        if not user_choice:
            speak("I didn't catch that.")
            return

        user_choice = user_choice.lower()
        filename, video_url = None, None

        # Check YOUTUBE_PRESETS
        for key, preset in YOUTUBE_PRESETS.items():
            if key in user_choice:
                filename = preset["filename"]
                video_url = preset["url"]
                break

        # No match — perform YouTube search
        if not filename or not video_url:
            query = urllib.parse.quote(user_choice)
            search_url = f"https://www.youtube.com/results?search_query={query}"
            speak(f"Searching YouTube for {user_choice}.")
            webbrowser.open(search_url)
            stop_music_vlc()
            return

        # Download if needed
        if not os.path.exists(filename):
            options = {
                'format': 'bestaudio/best',
                'noplaylist': True,
                'quiet': True,
                'outtmpl': filename
            }
            with YoutubeDL(options) as ydl:
                try:
                    ydl.download([video_url])
                    print(f"Downloaded audio as {filename}")
                except Exception as e:
                    print(f"Download error: {e}")
                    speak("Failed to download the requested music.")
                    return

        # Play music
        if os.path.exists(filename):
            player = vlc.MediaPlayer(filename)
            player.play()
            time.sleep(1)
        else:
            print("File missing after download attempt.")
            speak("Unable to find or play the downloaded music.")

    except Exception as e:
        print(f"Unexpected error: {e}")
        speak("Something went wrong while trying to play the music.")


def pause_music_vlc() -> None:
    """
    Toggle pause/resume on VLC player if active.
    """
    global player, music_paused
    try:
        if player:
            if player.is_playing():
                player.pause()
                music_paused = True
                print("Music paused.")
            elif music_paused:
                player.play()
                music_paused = False
                print("Music resumed.")
    except Exception as e:
        print(f"Error toggling playback: {e}")
        speak("An error occurred while toggling the music.")


def stop_music_vlc() -> None:
    """
    Stop music and reset player reference.
    """
    global player
    try:
        if player:
            player.stop()
            player = None
            print("Music stopped.")
        else:
            print("No music is currently playing.")
    except Exception as e:
        print(f"Error stopping music: {e}")
        speak("An error occurred while stopping the music.")


def set_vlc_volume(volume_level: int) -> None:
    """
    Set the VLC player's internal volume.

    Args:
        volume_level (int): Target volume (0–100).
    """
    global player
    try:
        if player:
            volume_level = max(0, min(100, volume_level))
            player.audio_set_volume(volume_level)
            print(f"VLC volume set to {volume_level}%")
    except Exception as e:
        print(f"Error setting volume: {e}")
        speak("Failed to set music volume.")
