import os
from yt_dlp import YoutubeDL
import vlc
import time

player = None  # Global VLC player instance
music_paused = False  # Global flag to track pause state

def play_youtube_music():
    global player
    
    # Your provided YouTube URL
    video_url = "https://www.youtube.com/watch?v=gn3vYlkxHpE"

    # Download/stream the best audio using yt-dlp
    options = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': 'audio.%(ext)s'
    }

    with YoutubeDL(options) as ydl:
        result = ydl.extract_info(video_url, download=True)
        filename = ydl.prepare_filename(result)

    # Use VLC to play audio
    if os.path.exists(filename):
        player = vlc.MediaPlayer(filename)
        player.play()
        time.sleep(1)  # Give some time to start playing
    else:
        print("Error: Audio file not found.")

def pause_music_vlc():
    global player, music_paused
    if player is not None:
        if player.is_playing() and not music_paused:
            player.pause()
            music_paused = True
            print("Music paused.")
        elif music_paused:
            player.play()
            music_paused = False
            print("Music resumed.")

def stop_music_vlc():
    global player
    if player is not None:
        player.stop()
        player = None
        print("Music stopped.")
    else:
        print("No music is currently playing.")


def set_vlc_volume(volume_level):
    """Set the volume of VLC player."""
    if player:
        # Volume level should be between 0 (mute) and 100 (max)
        volume_level = max(0, min(100, volume_level))
        player.audio_set_volume(volume_level)
        print(f"VLC volume set to {volume_level}%")  
