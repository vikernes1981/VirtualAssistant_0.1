import random
import webbrowser
from datetime import datetime
from entities import predict_intent, extract_entities
from feedback import handle_feedback
from speech import recognize_speech, speak
from browser import close_firefox_tab
from volume_control import get_volume, set_volume
from weather import get_weather
from news import get_news
from dictate import real_time_dictation
from youtube import play_youtube_music, stop_music_vlc, pause_music_vlc, set_vlc_volume  # Import the play_youtube_music function
from handle_notes import handle_notes

def process_command(command):
    global current_language  # Use global variables for language
    intent = predict_intent(command)
    print(f"Recognized intent: {intent}")
    entities = extract_entities(command)
    print("Extracted Entities:", entities)

    # Feedback Handling
    if intent in ["feedback_positive", "feedback_negative"]:
        handle_feedback(intent)
        pause_music_vlc()
        return  # Exit after handling feedback

    # Language switch command
    if intent == "switch_language":
        current_language = 'gr' if current_language == 'en' else 'en'  # Toggle between Greek and English
        response = "Μπορείς να μου μιλάς Ελληνικά τώρα." if current_language == 'gr' else "You can now talk to me in English."
        speak(response, response)  # Adjusted for dual-language response
        pause_music_vlc()
        return

    if intent == "close_tab":
        close_firefox_tab()  # Close the current tab using pyautogui
        pause_music_vlc()
        return

    # Dictation Command
    elif intent == "dictate_text":
        transcribed_text = real_time_dictation()  # Call the real-time dictation function
        print("\nFinal transcribed text:")
        print(transcribed_text)
        pause_music_vlc()
        return

    # Volume control commands
    elif intent == "volume_up":
        current_volume = get_volume()
        new_volume = min(current_volume + 10, 100)  # Increase volume by 10, max 100
        set_volume(new_volume)
        speak(f"Volume increased to {new_volume}%.", f"Η ένταση αυξήθηκε στο {new_volume}%.")
        pause_music_vlc()
    
    elif intent == "volume_down":
        current_volume = get_volume()
        new_volume = max(current_volume - 10, 0)  # Decrease volume by 10, min 0
        set_volume(new_volume)
        speak(f"Volume decreased to {new_volume}%.", f"Η ένταση μειώθηκε στο {new_volume}%.")
        pause_music_vlc()
    
    elif intent == "set_volume":
        try:
            # Extract volume level from entities if available
            level_entity = entities.get('PERCENT')  # Assuming 'PERCENT' is the key for the entity

            if level_entity and len(level_entity) > 0:
                # Extract and process the first value in the list
                level = int(level_entity[0].strip().replace("%", ""))  # Convert to integer and remove percentage symbol if present
                level = min(max(level, 0), 100)  # Ensure volume level is within 0-100%
                set_volume(level)
                speak(f"Volume set to {level}%.", f"Η ένταση ορίστηκε στο {level}%.")
            else:
                # If no level is found, prompt the user to specify
                speak("Please specify the volume level.", "Παρακαλώ καθορίστε την ένταση.")
        except (ValueError, TypeError) as e:
            # Handle the error if the conversion fails
            print(f"Error processing volume level: {e}")
            speak("I couldn't understand the volume level. Please specify a number.", "Δεν κατάλαβα την ένταση. Παρακαλώ καθορίστε έναν αριθμό.")
        pause_music_vlc()

    elif intent == "greet":
        speak("Hello! How can I help you?", "Γεια σου! Πώς μπορώ να σε βοηθήσω;")
        pause_music_vlc()

    elif intent == "get_time":
        current_time = datetime.now().strftime("%H:%M")
        speak(f"The current time is {current_time}.", f"Η τρέχουσα ώρα είναι {current_time}.")
        pause_music_vlc()

    elif intent == "get_date":
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {current_date}.", f"Σήμερα είναι {current_date}.")
        pause_music_vlc()

    elif intent == "get_weather":
        stralsund = "Stralsund"
        weather_info, weather_info_gr = get_weather(stralsund)
        speak(weather_info, weather_info_gr)
        pause_music_vlc()

    elif intent == "get_news":
        news_info_en, news_info_gr = get_news()  # Get both English and Greek news
        speak(news_info_en, news_info_gr)  # Speak out the news in both languages
        pause_music_vlc()

    elif intent == "open_website":
        speak("Please specify the website you want to open.", "Παρακαλώ καθορίσε την ιστοσελίδα που θέλεις να ανοίξεις.")
        website = recognize_speech()
        if website:
            url = f"https://{website.lower().replace(' ', '')}.com"
            webbrowser.open(url)
            speak(f"Opening {website}.", f"Άνοιγμα {website}.")
        pause_music_vlc()

    elif intent == "tell_joke":
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why don't skeletons fight each other? They don't have the guts."
        ]
        joke = random.choice(jokes)
        speak(joke, joke)  # Assuming similar structure for Greek jokes
        pause_music_vlc()

    elif intent == "farewell":
        speak("Goodbye! Have a great day.", "Αντίο! Να έχεις μια καλή μέρα.")
        pause_music_vlc()

    elif intent == "get_fact":
        facts = [
            "Honey never spoils.",
            "Bananas are berries, but strawberries aren't.",
            "There are more stars in the universe than grains of sand on all of Earth's beaches."
        ]
        fact = random.choice(facts)
        speak(fact, fact)  # Assuming similar structure for Greek facts
        pause_music_vlc()

    elif intent == "set_reminder":
        speak("You can add a reminder as a note. Let's manage your notes.", "Μπορείς να προσθέσεις μια υπενθύμιση ως σημείωση. Ας διαχειριστούμε τις σημειώσεις σου.")
        handle_notes()
        pause_music_vlc()

    elif intent == "tell_story":
        story = "Once upon a time in a faraway land, there lived a wise old owl..."
        speak(story, "Μια φορά και έναν καιρό σε μια μακρινή χώρα, ζούσε μια σοφή κουκουβάγια...")
        pause_music_vlc()

    elif intent == "play_music":
        speak("Playing some music now.", "Παίζω μουσική τώρα.")
        play_youtube_music()

    elif intent == "stop_music":
        stop_music_vlc()

    elif intent == "repeat":
        speak(command, command)  # Repeat the command spoken by the user
        pause_music_vlc()

    elif intent == "help":
        speak("I can help you with tasks like telling the weather, setting reminders, telling jokes, and more.", "Μπορώ να σε βοηθήσω με καθήκοντα όπως να λέω τον καιρό, να βάζω υπενθυμίσεις, να λέω ανέκδοτα και άλλα.")
        pause_music_vlc()
    elif intent == "music_volume":
    # Extract the number from the entities or from the command itself
        try:
            # Assuming 'number' is an extracted entity from the user's command
            # If using entities extraction:
            number_entity = entities.get('PERCENT')
            
            if number_entity and len(number_entity) > 0:
                # Extract and clean up the number (remove % if present)
                number = int(number_entity[0].strip().replace("%", ""))
            else:
                # Fallback: Extract number directly from the command (e.g., "music volume 30%")
                import re
                match = re.search(r'(\d+)', command)
                if match:
                    number = int(match.group(1))
                else:
                    raise ValueError("No volume level specified.")

            # Clamp the volume level between 0 and 100
            volume_level = max(0, min(100, number))
            set_vlc_volume(volume_level)
            speak(f"Music volume set to {volume_level}%.", f"Η ένταση μουσικής ορίστηκε στο {volume_level}%.")
            pause_music_vlc()
        except (ValueError, TypeError) as e:
            speak("I couldn't understand the volume level. Please specify a number.", "Δεν κατάλαβα την ένταση. Παρακαλώ καθορίστε έναν αριθμό.")
            pause_music_vlc()

    else:
        speak("I'm not sure how to respond to that. Please try again with different words.", "Δεν είμαι σίγουρος πώς να απαντήσω σε αυτό. Δοκίμασε ξανά με διαφορετικές λέξεις.")
        pause_music_vlc()
