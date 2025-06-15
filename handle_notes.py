from speech import recognize_speech, speak
from database import insert_note, get_all_notes, delete_note_by_id
from globals import number_map

def display_notes(notes: list) -> None:
    """
    Nicely formats and prints notes to terminal with spacing and borders.
    """
    print("\n\n========== 📝 YOUR NOTES ==========")
    for idx, note in enumerate(notes, start=1):
        print(f"Note {idx}: {note[1]}")
    print("===================================\n\n")

def handle_add_note(_: None, __: str) -> None:
    while True:
        msg = "Please say the note you'd like to add."
        print(f"[Assistant]: {msg}")
        speak(msg)

        note_content = recognize_speech()
        if note_content:
            if insert_note(note_content):
                msg = "Note added successfully."
            else:
                msg = "There was an error adding the note."
            print(f"[Assistant]: {msg}")
            speak(msg)

        msg = "Add another note or say exit."
        print(f"[Assistant]: {msg}")
        speak(msg)

        if "exit" in (recognize_speech() or "").lower():
            return

def handle_view_notes(_: None, __: str) -> None:
    while True:
        notes = get_all_notes()
        if notes:
            display_notes(notes)

            msg = "View your notes again or exit?"
            print(f"[Assistant]: {msg}")
            speak(msg)

            if "exit" in (recognize_speech() or "").lower():
                return
        else:
            msg = "You have no notes."
            print(f"[Assistant]: {msg}")
            speak(msg)
            return

def handle_delete_note(_: None, __: str) -> None:
    while True:
        notes = get_all_notes()
        if not notes:
            msg = "You have no notes to delete."
            print(f"[Assistant]: {msg}")
            speak(msg)
            return

        display_notes(notes)

        msg = "Please say the number of the note you'd like to delete."
        print(f"[Assistant]: {msg}")
        speak(msg)

        spoken = recognize_speech()
        note_number = number_map.get(spoken.lower(), spoken) if spoken else None

        if isinstance(note_number, int) and 1 <= note_number <= len(notes):
            note_id = notes[note_number - 1][0]
            if delete_note_by_id(note_id):
                msg = "Note deleted successfully."
            else:
                msg = "There was an error deleting the note."
        else:
            msg = "Invalid note number. Please try again."
        print(f"[Assistant]: {msg}")
        speak(msg)

        msg = "Delete another note or exit?"
        print(f"[Assistant]: {msg}")
        speak(msg)

        if "exit" in (recognize_speech() or "").lower():
            return
