"""
Performs a full system update using apt-get on Debian-based systems.
"""

import os
from speech import speak
import subprocess
from datetime import datetime



def handle_full_update(_: None, __: str) -> None:
    """
    Run full system update:
    - apt update
    - dist-upgrade
    - autoremove with purge
    """
    speak("Starting full system update. This may take a while.")
    print("🛠️ Running: apt update && dist-upgrade -y && autoremove -y\n")

    try:
        subprocess.run("sudo apt update && sudo apt dist-upgrade -y && sudo apt autoremove -y --purge", shell=True)

        speak("System update complete.")
        print("✅ System update finished successfully.")

        # Log the update
        with open("update.log", "a") as log:
            log.write(f"[{datetime.now()}] Full system update executed.\n")

    except Exception as e:
        print(f"Update error: {e}")
        speak("There was an error during the system update.")
