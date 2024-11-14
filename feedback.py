import sqlite3
from database import DATABASE_NAME
from speech import speak


def handle_feedback(intent):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    if intent == "feedback_positive":
        feedback_text = "User provided positive feedback."
        speak("Thank you for your feedback! I'm glad I could help.")
    elif intent == "feedback_negative":
        feedback_text = "User provided negative feedback."
        speak("I'm sorry to hear that. I'll try to improve!")

    cursor.execute('INSERT INTO feedback (intent, feedback) VALUES (?, ?)', (intent, feedback_text))
    conn.commit()
    conn.close()

def retrieve_feedback():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM feedback')
    rows = cursor.fetchall()
    
    for row in rows:
        print(f"ID: {row[0]}, Intent: {row[1]}, Feedback: {row[2]}")
    
    conn.close()
