"""
Handlers for opening and closing system applications like Sublime, Terminator, and Firefox.
"""

import os
from speech import speak


def open_sublime(_: None, __: str) -> None:
    """
    Open Sublime Text.
    """
    speak("Opening Sublime.")
    try:
        os.system("subl &")
    except Exception as e:
        print(f"Error opening Sublime: {e}")


def close_sublime(_: None, __: str) -> None:
    """
    Close all Sublime Text processes.
    """
    speak("Closing Sublime.")
    try:
        os.system("pkill -f sublime_text")
    except Exception as e:
        print(f"Error closing Sublime: {e}")


def open_terminator(_: None, __: str) -> None:
    """
    Open the Terminator terminal emulator.
    """
    speak("Opening Terminator.")
    try:
        os.system("terminator &")
    except Exception as e:
        print(f"Error opening Terminator: {e}")


def close_terminator(_: None, __: str) -> None:
    """
    Close all Terminator processes.
    """
    speak("Closing Terminator.")
    try:
        os.system("pkill -f terminator")
    except Exception as e:
        print(f"Error closing Terminator: {e}")


def open_virtualbox(_: None, __: str) -> None:
    """
    Launch VirtualBox.
    """
    speak("Opening VirtualBox.")
    try:
        os.system("virtualbox &")
    except Exception as e:
        print(f"Error opening VirtualBox: {e}")


def close_virtualbox(_: None, __: str) -> None:
    """
    Close all VirtualBox processes.
    """
    speak("Closing VirtualBox.")
    try:
        os.system("pkill -f virtualbox")
    except Exception as e:
        print(f"Error closing VirtualBox: {e}")


def close_firefox(_: None, __: str) -> None:
    """
    Close all Firefox browser windows.
    """
    speak("Closing Firefox.")
    try:
        os.system("pkill -f firefox")
    except Exception as e:
        print(f"Error closing Firefox: {e}")
