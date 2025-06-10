import time
import pyautogui
import webbrowser


def open_firefox_tab(url):
    """
    Opens the given URL in Firefox if available, otherwise falls back to default browser.
    """
    try:
        webbrowser.get("firefox").open(url)
        print(f"[✓] Opened URL in Firefox: {url}")
    except webbrowser.Error as e:
        print(f"[!] Firefox not available ({e}). Trying default browser...")
        try:
            webbrowser.open(url)
            print(f"[✓] Opened URL with fallback browser: {url}")
        except Exception as fallback_e:
            print(f"[✗] Failed to open URL: {fallback_e}")
    except Exception as e:
        print(f"[✗] Unexpected error: {e}")


def close_firefox_tab():
    """
    Closes the current Firefox tab by simulating 'Ctrl + W'.
    """
    try:
        time.sleep(0.5)
        pyautogui.hotkey("ctrl", "w")
        print("[✓] Firefox tab closed.")
    except pyautogui.FailSafeException:
        print("[!] PyAutoGUI fail-safe triggered (move mouse to corner).")
    except Exception as e:
        print(f"[✗] Failed to close tab: {e}")


def change_firefox_tab():
    """
    Switches to the next Firefox tab by simulating 'Ctrl + Tab'.
    """
    try:
        time.sleep(0.5)
        pyautogui.hotkey("ctrl", "tab")
        print("[✓] Switched Firefox tab.")
    except Exception as e:
        print(f"[✗] Failed to switch tab: {e}")
