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
