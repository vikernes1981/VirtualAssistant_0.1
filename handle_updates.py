"""
Performs a full system update using apt-get on Debian-based systems.
"""

import os
from speech import speak


def handle_full_update(_: None, __: str) -> None:
    """
    Run full system update:
    - apt update
    - dist-upgrade
    - autoremove with purge
    """
    speak("Running full system update.")
    try:
        os.system("sudo apt update && sudo apt dist-upgrade -y && sudo apt autoremove -y --purge")
    except Exception as e:
        print(f"Update error: {e}")
        speak("There was an error during the system update.")
