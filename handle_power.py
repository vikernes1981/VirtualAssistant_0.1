"""
System power control handlers for shutdown, reboot.
"""

import os
from speech import speak


def handle_shutdown(_: None, __: str) -> None:
    """
    Immediately shut down the system.
    """
    speak("Shutting down.")
    try:
        os.system("shutdown now")
    except Exception as e:
        print(f"Error during shutdown: {e}")


def handle_reboot(_: None, __: str) -> None:
    """
    Immediately reboot the system.
    """
    speak("Rebooting.")
    try:
        os.system("reboot")
    except Exception as e:
        print(f"Error during reboot: {e}")
