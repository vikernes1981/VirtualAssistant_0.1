import subprocess

# Volume Control Functions
def set_volume(level):
    try:
        if 0 <= level <= 100:
            subprocess.call(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{level}%"])
            print(f"Volume set to {level}%")
        else:
            print("Error: Volume level must be between 0 and 100.")
    except Exception as e:
        print(f"Error setting volume: {e}")

def get_volume():
    try:
        result = subprocess.run(["pactl", "get-sink-volume", "@DEFAULT_SINK@"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        output = result.stdout.decode()
        if output:
            try:
                # Attempt to extract the volume percentage
                current_volume = int(output.split()[4].strip('%'))
                return current_volume
            except (IndexError, ValueError) as parse_error:
                print(f"Error parsing volume level from output: {parse_error}")
                return None
        else:
            print("Error: No output received for current volume.")
            return None
    except subprocess.CalledProcessError as proc_error:
        print(f"Subprocess error: {proc_error}")
        return None
    except Exception as e:
        print(f"Unexpected error retrieving volume: {e}")
        return None
