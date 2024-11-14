import os
from gtts import gTTS
from speech import speak  # Assuming you have a `speak` function for text-to-speech
from ebooklib import epub
from bs4 import BeautifulSoup
import PyPDF2

def read_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            for i in range(num_pages):
                page = reader.pages[i]
                text = page.extract_text()
                if text:
                    speak(text)  # Call your speak function to read the text
                    input("Press Enter to continue to the next page...")
        print("Finished reading the PDF.")
    except FileNotFoundError:
        speak("The specified PDF file was not found.", "Το αρχείο PDF δεν βρέθηκε.")
        print("Error: File not found.")
    except Exception as e:
        speak("There was an error while reading the PDF.", "Υπήρξε σφάλμα κατά την ανάγνωση του PDF.")
        print(f"Error: {e}")

def read_text(file_path, language='en'):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Prepare text by removing or replacing newlines
        prepared_text = prepare_text_for_reading(content)

        # Split content into manageable chunks for reading (e.g., by paragraphs or sentences)
        chunks = prepared_text.split('.  ')  # Splitting by sentences for smoother reading
        
        for chunk in chunks:
            if chunk.strip():  # Only read non-empty chunks
                speak(chunk, None if language == 'en' else "")  # Adjust speak to work with your language setting
                input("Press Enter to continue reading...")  # Optional pause for user control
                
        print("Finished reading the book.")
    except FileNotFoundError:
        speak("The specified book file was not found.", "Το αρχείο του βιβλίου δεν βρέθηκε.")
        print("Error: File not found.")
    except Exception as e:
        speak("There was an error while reading the book.", "Υπήρξε σφάλμα κατά την ανάγνωση του βιβλίου.")
        print(f"Error: {e}")

def prepare_text_for_reading(text):
    # Replace all newlines with a space to ensure continuous reading
    return text.replace('\n', ' ')

def read_book(file_path, language='en'):
    if file_path.lower().endswith('.pdf'):
        read_pdf(file_path)
    elif file_path.lower().endswith('.txt'):
        read_text(file_path, language)
    else:
        speak("Unsupported file format.", "Μη υποστηριζόμενη μορφή αρχείου.")
        print("Error: Unsupported file format.")

# Example usage
read_book('book.txt')  # Replace with your actual file path
