import sqlite3

DATABASE_NAME = "feedback.db"  # Database name is hardcoded for SQLite

def create_feedback_table():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Create feedback table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY,
                intent TEXT,
                feedback TEXT
            )
        ''')

        # Create dictated_text table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dictated_text (
                id INTEGER PRIMARY KEY,
                text_content TEXT,
                language TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create notes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT
            )
        ''')

        conn.commit()
        print("Database tables created or verified successfully.")
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")
    except Exception as e:
        print(f"Unexpected error during table creation: {e}")
    finally:
        if conn:
            conn.close()

def insert_dictated_text(text, language):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO dictated_text (text_content, language)
            VALUES (?, ?)
        ''', (text, language))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"SQLite error saving text to database: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error saving text: {e}")
        return False
    finally:
        if conn:
            conn.close()

def insert_note(content):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO notes (content) VALUES (?)', (content,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"SQLite error inserting note: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error inserting note: {e}")
        return False
    finally:
        if conn:
            conn.close()

def get_all_notes():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT id, content FROM notes')
        notes = cursor.fetchall()
        return notes
    except sqlite3.Error as e:
        print(f"SQLite error fetching notes: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error fetching notes: {e}")
        return []
    finally:
        if conn:
            conn.close()

def delete_note_by_id(note_id):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"SQLite error deleting note: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error deleting note: {e}")
        return False
    finally:
        if conn:
            conn.close()
