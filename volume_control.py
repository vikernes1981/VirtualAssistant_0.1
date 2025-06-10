import subprocess

def set_volume(level):
    """
    Set the system volume to the specified percentage using pactl.
    Accepts values from 0 to 100.
    """

    try:
        if 0 <= level <= 100:
            subprocess.call(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{level}%"])
            print(f"Volume set to {level}%")
    except Exception as e:
        print(f"Error setting volume: {e}")

def get_volume():
    """
    Retrieve the current system volume percentage from the default sink.
    Returns an integer between 0–100 or 0 on failure.
    """

    try:
        result = subprocess.run(
            ["pactl", "get-sink-volume", "@DEFAULT_SINK@"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        output = result.stdout.decode()
        return int(output.split()[4].strip('%')) if output else None
    except Exception as e:
        print(f"Error retrieving volume: {e}")
        return 0
