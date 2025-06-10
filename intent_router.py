from handle_notes import (
    handle_add_note, handle_view_notes, handle_delete_note
)
from main_commands import (
    handle_greeting, handle_time, handle_date, handle_weather, handle_open_website,
    handle_farewell, handle_audiobook, handle_play_music, handle_stop_music,
    handle_music_volume, handle_dictation, handle_close_tab, handle_set_volume,
    handle_volume_up, handle_volume_down
)
from help_command import handle_help

def get_handler(intent):
    return {
        "greeting": handle_greeting,
        "time": handle_time,
        "date": handle_date,
        "weather": handle_weather,
        "open_website": handle_open_website,
        "farewell": handle_farewell,
        "audiobook": handle_audiobook,
        "play_music": handle_play_music,
        "stop_music": handle_stop_music,
        "music_volume": handle_music_volume,
        "dictate_text": handle_dictation,
        "close_tab": handle_close_tab,
        "set_volume": handle_set_volume,
        "volume_up": handle_volume_up,
        "volume_down": handle_volume_down,
        "add_note": handle_add_note,
        "create_note": handle_add_note,
        "note": handle_add_note,
        "view_notes": handle_view_notes,
        "show_notes": handle_view_notes,
        "list_notes": handle_view_notes,
        "delete_note": handle_delete_note,
        "remove_note": handle_delete_note,
        "help": handle_help,
    }.get(intent)
