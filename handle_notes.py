"""
Voice-controlled note management for the Virtual Assistant.

Allows users to create, view, and delete notes using natural speech input.
"""

from speech import recognize_speech, speak
from database import insert_note, get_all_notes, delete_note_by_id
from globals import number_map


def handle_add_note(_: None, __: str) -> None:
    """
    Prompt user to speak one or more notes, and store them in the database.
    Stops when the user says "exit".
    """
    while True:
        speak("Please say the note you'd like to add.")
        note_content = recognize_speech()
        if note_content:
            if insert_note(note_content):
                speak("Note added successfully.")
            else:
                speak("There was an error adding the note.")
        speak("Add another note or say exit.")
        if "exit" in (recognize_speech() or "").lower():
            return


def handle_view_notes(_: None, __: str) -> None:
    """
    Read all saved notes aloud.
    Repeats until the user says "exit" or if there are no notes.
    """
    while True:
        notes = get_all_notes()
        if notes:
            print("Here are your notes:")
            for idx, note in enumerate(notes, start=1):
                print(f"Note {idx}: {note[1]}")
            speak("View your notes again or exit?")
            if "exit" in (recognize_speech() or "").lower():
                return
        else:
            speak("You have no notes.")
            return


def handle_delete_note(_: None, __: str) -> None:
    """
    Allow the user to delete notes by speaking their number.
    Stops when the user says "exit" or all notes are deleted.
    """
    while True:
        notes = get_all_notes()
        if not notes:
            speak("You have no notes to delete.")
            return

        print("Here are your notes:")
        for idx, note in enumerate(notes, start=1):
            print(f"Note {idx}: {note[1]}")

        speak("Please say the number of the note you'd like to delete.")
        spoken = recognize_speech()
        note_number = number_map.get(spoken.lower(), spoken) if spoken else None

        if isinstance(note_number, int) and 1 <= note_number <= len(notes):
            note_id = notes[note_number - 1][0]
            if delete_note_by_id(note_id):
                speak("Note deleted successfully.")
            else:
                speak("There was an error deleting the note.")
        else:
            speak("Invalid note number. Please try again.")

        speak("Delete another note or exit?")
        if "exit" in (recognize_speech() or "").lower():
            return
