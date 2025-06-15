from handle_notes import (
    handle_add_note, handle_view_notes, handle_delete_note
)
from main_commands import (
    handle_greeting, handle_time, handle_date, handle_weather, handle_open_website,
    handle_farewell, handle_audiobook, handle_play_music, handle_stop_music,
    handle_music_volume, handle_dictation, handle_close_tab, handle_set_volume,
    handle_volume_up, handle_volume_down
)
from handle_updates import handle_full_update
from handle_apps import (
    open_sublime, close_sublime, open_terminator, close_terminator,
    open_virtualbox, close_virtualbox, close_firefox
)
from handle_power import handle_shutdown, handle_reboot
from help_command import handle_help

def get_handler(intent):
    return {
        # Notes-related intents
        "add_note": handle_add_note,
        "create_note": handle_add_note,
        "note": handle_add_note,
        "delete_note": handle_delete_note,
        "remove_note": handle_delete_note,
        "list_notes": handle_view_notes,
        "show_notes": handle_view_notes,
        "view_notes": handle_view_notes,

        # Music and audio
        "audiobook": handle_audiobook,
        "tell_me_a_story": handle_audiobook,
        "play_music": handle_play_music,
        "stop_music": handle_stop_music,
        "music_volume": handle_music_volume,
        "set_volume": handle_set_volume,
        "volume_up": handle_volume_up,
        "volume_down": handle_volume_down,

        # System commands
        "shutdown": handle_shutdown,
        "reboot": handle_reboot,
        "system_update": handle_full_update,

        # Application control
        "open_sublime": open_sublime,
        "close_sublime": close_sublime,
        "open_terminator": open_terminator,
        "close_terminator": close_terminator,
        "open_virtualbox": open_virtualbox,
        "close_virtualbox": close_virtualbox,
        "close_firefox": close_firefox,

        # Web and browser
        "open_website": handle_open_website,
        "close_tab": handle_close_tab,

        # Utilities
        "dictate_text": handle_dictation,

        # Date and time
        "date": handle_date,
        "time": handle_time,

        # Weather
        "weather": handle_weather,

        # Greetings and help
        "greeting": handle_greeting,
        "farewell": handle_farewell,
        "help": handle_help,
    }.get(intent)
