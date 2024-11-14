import pvporcupine
import pyaudio
import numpy as np
import os
from dotenv import load_dotenv
from youtube import pause_music_vlc  # Import the pause_music_vlc function

# Load environment variables
load_dotenv()

def listen_for_wake_word(model_path):
    access_key = os.getenv("PORCUPINE_ACCESS_KEY")  # Load from .env file
    porcupine = pvporcupine.create(keywords=["jarvis"], access_key=access_key)
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(rate=porcupine.sample_rate,
                           channels=1,
                           format=pyaudio.paInt16,
                           input=True,
                           frames_per_buffer=512)

    print("Listening for wake word...")
    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = np.frombuffer(pcm, dtype=np.int16)
        result = porcupine.process(pcm)
        if result >= 0:
            pause_music_vlc()
            print("Wake word detected!")
            return  # Exit the loop to trigger the assistant's main functionality
