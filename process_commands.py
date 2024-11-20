import webbrowser
from datetime import datetime
from entities import predict_intent, extract_entities
from feedback import handle_feedback
from speech import recognize_speech, speak
from browser import close_firefox_tab
from volume_control import set_volume, get_volume
from weather import get_weather
from news import fetch_and_process_news
from dictate import real_time_dictation
from youtube import play_youtube_music, stop_music_vlc, pause_music_vlc, set_vlc_volume
from handle_notes import process_user_command as handle_notes
from globals import current_language
from readBook import select_and_play_audiobook
from jokes import get_random_joke
from facts import get_random_fact

def process_command(command):
    global current_language  # Use global variables for language
    try:
        intent = predict_intent(command)
        print(f"Recognized intent: {intent}")
        entities = extract_entities(command)
        print("Extracted Entities:", entities)

        # Feedback Handling
        if intent in ["feedback_positive", "feedback_negative"]:
            handle_feedback(intent)
            pause_music_vlc()
            return  # Exit after handling feedback

        if intent == "close_tab":
            try:
                close_firefox_tab()  # Close the current tab using pyautogui
            except Exception as e:
                print(f"Error closing tab: {e}")
                speak("There was an error closing the tab.", "Υπήρξε σφάλμα κατά το κλείσιμο της καρτέλας.")
            pause_music_vlc()
            return

        # Dictation Command
        elif intent == "dictate_text":
            try:
                transcribed_text = real_time_dictation()  # Call the real-time dictation function
                print("\nFinal transcribed text:")
                print(transcribed_text)
            except Exception as e:
                print(f"Error during dictation: {e}")
                speak("There was an error during dictation.", "Υπήρξε σφάλμα κατά τη δικτατορία.")
            pause_music_vlc()
            return

        # Volume control commands
        elif intent == "volume_up":
            try:
                current_volume = get_volume()
                new_volume = min(current_volume + 10, 100)  # Increase volume by 10, max 100
                set_volume(new_volume)
                speak(f"Volume increased to {new_volume}%.", f"Η ένταση αυξήθηκε στο {new_volume}%.")
            except Exception as e:
                print(f"Error adjusting volume: {e}")
                speak("There was an error adjusting the volume.", "Υπήρξε σφάλμα κατά τη ρύθμιση της έντασης.")
            pause_music_vlc()

        elif intent == "volume_down":
            try:
                current_volume = get_volume()
                new_volume = max(current_volume - 10, 0)  # Decrease volume by 10, min 0
                set_volume(new_volume)
                speak(f"Volume decreased to {new_volume}%.", f"Η ένταση μειώθηκε στο {new_volume}%.")
            except Exception as e:
                print(f"Error adjusting volume: {e}")
                speak("There was an error adjusting the volume.", "Υπήρξε σφάλμα κατά τη ρύθμιση της έντασης.")
            pause_music_vlc()

        elif intent == "set_volume":
            try:
                # Extract volume level from entities if available
                level_entity = entities.get('PERCENT')
                if level_entity and len(level_entity) > 0:
                    level = int(level_entity[0].strip().replace("%", ""))
                    level = min(max(level, 0), 100)
                    set_volume(level)
                    speak(f"Volume set to {level}%.", f"Η ένταση ορίστηκε στο {level}%.")
                else:
                    speak("Please specify the volume level.", "Παρακαλώ καθορίστε την ένταση.")
            except (ValueError, TypeError) as e:
                print(f"Error processing volume level: {e}")
                speak("I couldn't understand the volume level. Please specify a number.", "Δεν κατάλαβα την ένταση. Παρακαλώ καθορίστε έναν αριθμό.")
            pause_music_vlc()

        elif intent == "greet":
            speak("Hello! How can I help you?", "Γεια σου! Πώς μπορώ να σε βοηθήσω;")
            pause_music_vlc()

        elif intent == "get_time":
            try:
                current_time = datetime.now().strftime("%H:%M")
                speak(f"The current time is {current_time}.", f"Η τρέχουσα ώρα είναι {current_time}.")
            except Exception as e:
                print(f"Error getting time: {e}")
                speak("There was an error getting the current time.", "Υπήρξε σφάλμα κατά την απόκτηση της τρέχουσας ώρας.")
            pause_music_vlc()

        elif intent == "get_date":
            try:
                current_date = datetime.now().strftime("%A, %B %d, %Y")
                speak(f"Today is {current_date}.", f"Σήμερα είναι {current_date}.")
            except Exception as e:
                print(f"Error getting date: {e}")
                speak("There was an error getting the date.", "Υπήρξε σφάλμα κατά την απόκτηση της ημερομηνίας.")
            pause_music_vlc()

        elif intent == "get_weather":
            try:
                stralsund = "Stralsund"
                weather_info, weather_info_gr = get_weather(stralsund)
                speak(weather_info, weather_info_gr)
            except Exception as e:
                print(f"Error fetching weather: {e}")
                speak("There was an error fetching the weather.", "Υπήρξε σφάλμα κατά την αναζήτηση του καιρού.")
            pause_music_vlc()

        elif intent == "get_news":
            try:
                # Fetch news using the `fetch_and_process_news` function
                news_list = fetch_and_process_news()
                
                if news_list:
                    # Speak each news item
                    for idx, (title, summary) in enumerate(news_list, start=1):
                        print(f"News {idx}:")
                        print(f"  Title: {title}")
                        print(f"  Summary: {summary}")
                        speak(f"News {idx}: {title}. {summary}.", 
                              f"Νέα {idx}: {title}. {summary}.")
                else:
                    speak("No news articles were found.", "Δεν βρέθηκαν ειδήσεις.")
            except Exception as e:
                print(f"Error fetching news: {e}")
                speak("There was an error fetching the news.", "Υπήρξε σφάλμα κατά την αναζήτηση ειδήσεων.")
            
            # Pause music if VLC is active
            pause_music_vlc()


        elif intent == "open_website":
            speak("Please specify the website you want to open.", "Παρακαλώ καθορίσε την ιστοσελίδα που θέλεις να ανοίξεις.")
            website = recognize_speech()
            if website:
                try:
                    url = f"https://{website.lower().replace(' ', '')}.com"
                    webbrowser.open(url)
                    speak(f"Opening {website}.", f"Άνοιγμα {website}.")
                except Exception as e:
                    print(f"Error opening website: {e}")
                    speak("There was an error opening the website.", "Υπήρξε σφάλμα κατά το άνοιγμα της ιστοσελίδας.")
            pause_music_vlc()

        elif intent == "tell_joke":
            try:
                joke = get_random_joke()
                speak(joke)
            except Exception as e:
                print(f"Error fetching joke: {e}")
                speak("There was an error fetching a joke.", "Υπήρξε σφάλμα κατά την αναζήτηση ενός ανέκδοτου.")
            pause_music_vlc()

        elif intent == "farewell":
            speak("Goodbye! Have a great day.", "Αντίο! Να έχεις μια καλή μέρα.")
            pause_music_vlc()

        elif intent == "get_fact":
            try:
                fact = get_random_fact()
                speak(fact)
            except Exception as e:
                print(f"Error fetching fact: {e}")
                speak("There was an error fetching a fact.", "Υπήρξε σφάλμα κατά την αναζήτηση μιας ενδιαφέρουσας πληροφορίας.")
            pause_music_vlc()

        elif intent == "set_reminder":
            speak("You can add a reminder as a note.")
            handle_notes()
            pause_music_vlc()

        elif intent == "tell_story":
            try:
                select_and_play_audiobook()
            except Exception as e:
                print(f"Error playing audiobook: {e}")
                speak("There was an error playing the audiobook.", "Υπήρξε σφάλμα κατά την αναπαραγωγή του ακουστικού βιβλίου.")
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
            try:
                number_entity = entities.get('PERCENT')
                if number_entity and len(number_entity) > 0:
                    number = int(number_entity[0].strip().replace("%", ""))
                else:
                    import re
                    match = re.search(r'(\d+)', command)
                    if match:
                        number = int(match.group(1))
                    else:
                        raise ValueError("No volume level specified.")
                volume_level = max(0, min(100, number))
                set_vlc_volume(volume_level)
                speak(f"Music volume set to {volume_level}%.", f"Η ένταση μουσικής ορίστηκε στο {volume_level}%.")
            except (ValueError, TypeError) as e:
                print(f"Error setting music volume: {e}")
                speak("I couldn't understand the volume level. Please specify a number.", "Δεν κατάλαβα την ένταση. Παρακαλώ καθορίστε έναν αριθμό.")
                pause_music_vlc()

        else:
            speak("I'm not sure how to respond to that. Please try again with different words.", "Δεν είμαι σίγουρος πώς να απαντήσω σε αυτό. Δοκίμασε ξανά με διαφορετικές λέξεις.")
            pause_music_vlc()

    except Exception as e:
        print(f"Unexpected error during command processing: {e}")
        speak("An unexpected error occurred while processing your command.", "Προέκυψε απρόσμενο σφάλμα κατά την επεξεργασία της εντολής σου.")
