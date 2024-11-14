import subprocess

# Volume Control Functions
def set_volume(level):
    subprocess.call(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{level}%"])

def get_volume():
    result = subprocess.run(["pactl", "get-sink-volume", "@DEFAULT_SINK@"], stdout=subprocess.PIPE)
    output = result.stdout.decode()
    current_volume = int(output.split()[4].strip('%'))  # The volume percentage is the 5th word
    return current_volume