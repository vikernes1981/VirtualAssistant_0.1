from datetime import datetime
from speech import speak, recognize_speech
from browser import close_firefox_tab
from dictate import real_time_dictation
from weather import get_weather
from youtube import (
    play_youtube_music, stop_music_vlc, pause_music_vlc, set_vlc_volume
)
from volume_control import set_volume, get_volume
from read_book import select_and_play_audiobook

def handle_greeting(_, __): speak("Hello! How can I help you?")
def handle_time(_, __):
    current_time = datetime.now().strftime('%H:%M')
    print(f"Current time: {current_time}")
    speak(f"The current time is {current_time}.")

def handle_date(_, __):
    current_date = datetime.now().strftime('%A, %B %d, %Y')
    print(f"Current date: {current_date}")
    speak(f"Today is {current_date}.")
def handle_close_tab(_, __): close_firefox_tab(); pause_music_vlc()
def handle_dictation(_, __): transcribed = real_time_dictation(); print("Dictation result:", transcribed); pause_music_vlc()
def handle_volume_up(_, __): vol = min(get_volume() + 10, 100); set_volume(vol); speak(f"Volume increased to {vol}%"); pause_music_vlc()
def handle_volume_down(_, __): vol = max(get_volume() - 10, 0); set_volume(vol); speak(f"Volume decreased to {vol}%"); pause_music_vlc()
def handle_set_volume(entities, command):
    import re
    try:
        level_str = entities.get("PERCENT", [None])[0] if entities else None
        if not level_str:
            match = re.search(r'\b(\d{1,3})\b', command)
            level_str = match.group(1) if match else None
        if level_str is None:
            raise ValueError
        level = int(level_str.strip().replace("%", ""))
        level = max(0, min(100, level))
        set_volume(level)
        speak(f"Volume set to {level}%.")
    except Exception as e:
        print(f"Volume set error: {e}")
        speak("I couldn't understand the volume level.")
    pause_music_vlc()
def handle_weather(_, __): info = get_weather("Stralsund"); speak(info); pause_music_vlc()
def handle_open_website(_, __): speak("Please specify the website."); import webbrowser; site = recognize_speech(); webbrowser.open(f"https://{site.lower().replace(' ', '')}.com"); speak(f"Opening {site}"); pause_music_vlc()
def handle_farewell(_, __): speak("Goodbye! Have a great day."); pause_music_vlc()
def handle_audiobook(_, __): select_and_play_audiobook(); pause_music_vlc()
def handle_play_music(_, __): speak("Playing some music now."); play_youtube_music()
def handle_stop_music(_, __): stop_music_vlc()
def handle_music_volume(entities, command):
    import re
    try:
        level_str = entities.get("PERCENT", [None])[0] if entities else None
        if not level_str:
            match = re.search(r'(\d+)', command)
            level_str = match.group(1) if match else None
        level = int(level_str)
        level = max(0, min(100, level))
        set_vlc_volume(level)
        speak(f"Music volume set to {level}%.")
    except Exception as e:
        print(f"Music volume error: {e}")
        speak("I couldn't understand the music volume level.")
    pause_music_vlc()
