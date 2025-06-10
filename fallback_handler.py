"""
Fallback handler for command overrides in the Virtual Assistant.

This module intercepts certain keywords in user commands and bypasses
AI intent routing by directly invoking mapped system/app handlers.
"""

from speech import speak
from handle_updates import handle_full_update
from handle_apps import (
    open_sublime, close_sublime, open_terminator, close_terminator,
    open_virtualbox, close_virtualbox, close_firefox
)
from handle_power import (
    handle_shutdown, handle_reboot
)
from youtube import pause_music_vlc
from globals import KEYWORD_INTENT_MAP

# Mapping of known fallback intents to their corresponding handler functions
INTENT_ROUTER = {
    "shutdown": handle_shutdown,
    "reboot": handle_reboot,
    "update_system": handle_full_update,
    "open_sublime": open_sublime,
    "close_sublime": close_sublime,
    "open_terminator": open_terminator,
    "close_terminator": close_terminator,
    "open_virtualbox": open_virtualbox,
    "close_virtualbox": close_virtualbox,
    "close_firefox": close_firefox,
}

def handle_unknown(_, command, override=False):
    """
    Intercept and handle known keyword-based commands without relying on AI intent detection.

    Args:
        _ (unused): Placeholder for entities, not used in fallback.
        command (str): The raw user command as a string.
        override (bool): If True, this function short-circuits the AI and checks for direct matches.

    Returns:
        bool: True if a matching fallback was handled, otherwise False.
    """
    cmd = command.lower()
    if override:
        print(f"[✓] Override fallback triggered: {cmd}")
        for keyword, intent in KEYWORD_INTENT_MAP.items():
            if keyword in cmd:
                handler = INTENT_ROUTER.get(intent)
                if handler:
                    handler(None, command)
                    return True
        return False

    speak("I'm not sure how to respond to that. Please try again.")
    pause_music_vlc()
