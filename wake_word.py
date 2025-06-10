import pvporcupine
import pyaudio
import numpy as np
import os
from dotenv import load_dotenv
from youtube import pause_music_vlc  # Import the pause_music_vlc function
import time
# Load environment variables
load_dotenv()

def listen_for_wake_word(model_path):
    """
    Continuously listen to the microphone for a specific wake word using Porcupine.
    Pauses music and returns once the keyword is detected.
    """

    access_key = os.getenv("PORCUPINE_ACCESS_KEY")  # Load from .env file

    porcupine = pvporcupine.create(
        access_key=access_key,
        keyword_paths=[model_path]  # Use your .ppn file path here
    )

    pa = pyaudio.PyAudio()
    audio_stream = pa.open(rate=porcupine.sample_rate,
                           channels=1,
                           format=pyaudio.paInt16,
                           input=True,
                           frames_per_buffer=512)

    print("Listening for wake word...")
    while True:
        pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm = np.frombuffer(pcm, dtype=np.int16)
        result = porcupine.process(pcm)
        if result >= 0:
            start_time = time.time()
            pause_music_vlc()
            print("Wake word detected!")
            print(f"Operation took {time.time() - start_time:.2f} seconds")
            return  # Wake word detected
