import webbrowser
import time
import pyautogui

# Function to open a website in Firefox with the specified profile
def open_firefox_tab(url):
    # Open the URL using the default browser (Firefox, if set as default)
    webbrowser.get("firefox").open(url)
    print(f"Opened {url} in Firefox.")

# Function to close the current tab
def close_firefox_tab():
    time.sleep(2)  # Adjust this sleep time as needed
    # Simulate pressing 'Ctrl + W' to close the current Firefox tab (on Windows/Linux)
    pyautogui.hotkey("ctrl", "w")
    print("Firefox tab closed successfully.")
