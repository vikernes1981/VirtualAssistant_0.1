"""
Handles all SQLite database operations for the Virtual Assistant.

Includes functions for initializing tables, inserting and retrieving notes,
and saving dictated text entries.
"""

import sqlite3
from globals import DATABASE_NAME


def initialize_database() -> None:
    """
    Create necessary tables for dictated text and notes if they do not exist.
    """
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dictated_text (
                    id INTEGER PRIMARY KEY,
                    text_content TEXT,
                    language TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            conn.commit()
            print("Database tables created or verified successfully.")
    except sqlite3.Error as e:
        print(f"SQLite error during initialization: {e}")
    except Exception as e:
        print(f"Unexpected error during initialization: {e}")


def insert_dictated_text(text: str, language: str) -> bool:
    """
    Save a dictated text entry into the database.

    Args:
        text (str): The transcribed text.
        language (str): The language code of the transcription.

    Returns:
        bool: True if insertion was successful, else False.
    """
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO dictated_text (text_content, language) VALUES (?, ?)',
                (text, language)
            )
            conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"SQLite error saving dictated text: {e}")
    except Exception as e:
        print(f"Unexpected error saving dictated text: {e}")
    return False


def insert_note(content: str) -> bool:
    """
    Insert a note into the notes table.

    Args:
        content (str): The note content.

    Returns:
        bool: True if the note was successfully saved, else False.
    """
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO notes (content) VALUES (?)', (content,))
            conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"SQLite error inserting note: {e}")
    except Exception as e:
        print(f"Unexpected error inserting note: {e}")
    return False


def get_all_notes() -> list[tuple[int, str]]:
    """
    Retrieve all saved notes from the database.

    Returns:
        list of tuples: Each tuple contains (id, content) for a note.
    """
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, content FROM notes')
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"SQLite error fetching notes: {e}")
    except Exception as e:
        print(f"Unexpected error fetching notes: {e}")
    return []


def delete_note_by_id(note_id: int) -> bool:
    """
    Delete a note by its ID.

    Args:
        note_id (int): The ID of the note to delete.

    Returns:
        bool: True if the deletion was successful, else False.
    """
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
            conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"SQLite error deleting note: {e}")
    except Exception as e:
        print(f"Unexpected error deleting note: {e}")
    return False
