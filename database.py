import sqlite3

DATABASE_NAME = "feedback.db"  # Database name is hardcoded for SQLite

def create_feedback_table():
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
    
    conn.commit()
    conn.close()


    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT
        )
    ''')
    conn.commit()
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
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving text to database: {e}")
        return False

# Add these functions to your `database.py` file
def insert_note(content):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO notes (content) VALUES (?)', (content,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error inserting note: {e}")
        return False

def get_all_notes():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, content FROM notes')
    notes = cursor.fetchall()
    conn.close()
    return notes

def delete_note_by_id(note_id):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting note: {e}")
        return False
