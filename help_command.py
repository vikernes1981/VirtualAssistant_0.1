"""
Dynamically generates and speaks a list of available assistant commands.
"""

from speech import speak
from globals import KEYWORD_INTENT_MAP


def handle_help(_: None, __: str) -> None:
    """
    Speak and print the dynamically generated list of available assistant commands.
    """
    speak("Here are the commands I currently support.")
    print("\nAvailable Commands:\n")

    # Group commands by rough category
    groups = {
        "📝 Notes": [],
        "🎵 Music & Audio": [],
        "🔊 Volume": [],
        "🗣 Dictation": [],
        "📚 Audiobooks": [],
        "🕒 Info": [],
        "🌐 Web": [],
        "🖥 App Control": [],
        "🧠 System Power": [],
        "⬆️ Updates": [],
        "👋 General": [],
    }

    # Scan known intents
    for keyword, intent in KEYWORD_INTENT_MAP.items():
        if intent == "add_note" or "note" in intent:
            groups["📝 Notes"].append(keyword)
        elif "music" in intent or "audiobook" in intent:
            groups["🎵 Music & Audio"].append(keyword)
        elif "volume" in intent:
            groups["🔊 Volume"].append(keyword)
        elif "dictate" in intent:
            groups["🗣 Dictation"].append(keyword)
        elif "weather" in intent or "time" in intent or "date" in intent:
            groups["🕒 Info"].append(keyword)
        elif "website" in intent or "tab" in intent:
            groups["🌐 Web"].append(keyword)
        elif "sublime" in intent or "terminator" in intent or "virtualbox" in intent or "firefox" in intent:
            groups["🖥 App Control"].append(keyword)
        elif intent in {"shutdown", "reboot"}:
            groups["🧠 System Power"].append(keyword)
        elif "update" in intent:
            groups["⬆️ Updates"].append(keyword)
        elif intent in {"greeting", "farewell", "help"}:
            groups["👋 General"].append(keyword)

    # Output help text
    for category, commands in groups.items():
        if commands:
            print(f"{category}")
            for cmd in sorted(set(commands)):
                print(f"  - {cmd}")
            print()

    speak("Let me know what you'd like to try.")
