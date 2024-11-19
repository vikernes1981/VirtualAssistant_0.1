import webbrowser
import time
import pyautogui

def open_firefox_tab(url):
    """Open a website in Firefox using the default browser profile."""
    try:
        webbrowser.get("firefox").open(url)
        print(f"Opened {url} in Firefox.")
    except webbrowser.Error as e:
        print(f"Error opening {url} in Firefox: {e}")
        print("Please ensure Firefox is installed and set as the default browser.")
    except Exception as e:
        print(f"Unexpected error opening {url}: {e}")

def close_firefox_tab():
    """Close the current Firefox tab by simulating 'Ctrl + W' keypress."""
    try:
        time.sleep(2)  # Adjust this sleep time as needed
        pyautogui.hotkey("ctrl", "w")
        print("Firefox tab closed successfully.")
    except pyautogui.FailSafeException:
        print("PyAutoGUI fail-safe triggered. Move the mouse to the corner of the screen to avoid unintended actions.")
    except Exception as e:
        print(f"Unexpected error while closing the Firefox tab: {e}")
