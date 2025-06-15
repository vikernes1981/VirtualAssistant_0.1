"""
Global constants and shared configuration for the Virtual Assistant.

This module centralizes environment-independent values such as paths,
intent keyword fallbacks, and global recognizer instances.
"""

import os
import speech_recognition as sr

#: Single shared recognizer instance for the app
recognizer = sr.Recognizer()

#: Maps spoken number words or digits to integers (1–10)
number_map = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
    "twenty one": 21, "twenty-two": 22, "twenty three": 23, "twenty four": 24, "twenty five": 25,
    "twenty six": 26, "twenty seven": 27, "twenty eight": 28, "twenty nine": 29, "thirty": 30,
    "thirty one": 31, "thirty two": 32, "thirty three": 33, "thirty four": 34, "thirty five": 35,
    "thirty six": 36, "thirty seven": 37, "thirty eight": 38, "thirty nine": 39, "forty": 40,
    "1": 1, "2": 2, "3": 3, "4": 4, "5": 5,
    "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
    "11": 11, "12": 12, "13": 13, "14": 14, "15": 15,
    "16": 16, "17": 17, "18": 18, "19": 19, "20": 20,
    "21": 21, "22": 22, "23": 23, "24": 24, "25": 25,
    "26": 26, "27": 27, "28": 28, "29": 29, "30": 30,
    "31": 31, "32": 32, "33": 33, "34": 34, "35": 35,
    "36": 36, "37": 37, "38": 38, "39": 39, "40": 40
}

#: Path to SQLite database
DATABASE_NAME = "assistant.db"

#: File for temporary dictation monitoring
DICTATION_FILE = "dictation.txt"

#: Path to wake word model file (Porcupine .ppn)
WAKE_WORD_MODEL_PATH = "./porcupine_models/jarvis_linux.ppn"

#: Default city used in weather queries
DEFAULT_WEATHER_CITY = "Stralsund"

#: OpenAI Whisper model name used for transcription
WHISPER_MODEL = "whisper-1"

#: GPT model name used for intent and language generation
GPT_MODEL = "gpt-3.5-turbo"

#: JSON file for storing audiobook playback resume points
PLAYBACK_STATE_FILE = "playback_positions.json"

#: Default browser used in web automation
DEFAULT_BROWSER = "firefox"

#: Preset YouTube music shortcuts
YOUTUBE_PRESETS = {
    "relax": {
        "filename": "lofi_audio.m4a",
        "url": "https://www.youtube.com/watch?v=sF80I-TQiW0"
    },
    "warcraft": {
        "filename": "warcraft_audio.m4a",
        "url": "https://www.youtube.com/watch?v=ebmwJnhtMgY"
    }
}

#: Maps known keywords to corresponding internal assistant intents
KEYWORD_INTENT_MAP = {
    # --- Notes ---
    "note": "add_note",
    "notes": "view_notes",
    "add note": "add_note",
    "view note": "view_notes",
    "delete note": "delete_note",
    "remove note": "delete_note",

    # --- Music ---
    "music": "play_music",
    "play music": "play_music",
    "stop music": "stop_music",
    "pause": "stop_music",
    "resume": "play_music",
    "song": "play_music",
    "listen": "play_music",

    # --- Volume ---
    "louder": "volume_up",
    "increase volume": "volume_up",
    "turn up": "volume_up",
    "turn up volume": "volume_up",
    "raise volume": "volume_up",
    "quieter": "volume_down",
    "decrease volume": "volume_down",
    "turn volume down": "volume_down",
    "turn down the volume": "volume_down",
    "lower volume": "volume_down",
    "mute": "set_volume",

    # --- Audiobooks ---
    "audiobook": "audiobook",
    "read": "audiobook",
    "book": "audiobook",

    # --- Dictation ---
    "dictate": "dictate_text",
    "dictation": "dictate_text",

    # --- System Info ---
    "time": "time",
    "date": "date",
    "weather": "weather",

    # --- Websites ---
    "website": "open_website",
    "open website": "open_website",
    "browse": "open_website",

    # --- Greetings & Farewell ---
    "hello": "greeting",
    "hi": "greeting",
    "hey": "greeting",
    "goodbye": "farewell",
    "bye": "farewell",
    "exit": "farewell",
    "quit": "farewell",

    # --- Help ---
    "help": "help",
    "commands": "help",
    "what can you do": "help",

    # --- Power Management ---
    "shutdown": "shutdown",
    "reboot": "reboot",
    "restart": "reboot",

    # --- System Updates ---
    "update system": "system_update",
    "full update": "system_update",
    "system upgrade": "system_update",
    "upgrade": "system_update",

    # --- App Control ---
    "open sublime": "open_sublime",
    "close sublime": "close_sublime",
    "open terminal": "open_terminator",
    "close terminal": "close_terminator",
    "open virtualbox": "open_virtualbox",
    "close virtualbox": "close_virtualbox",
    "close firefox": "close_firefox",
}
