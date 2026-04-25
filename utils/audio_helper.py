import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from core import config

class AudioHelper:
    @staticmethod
    def record_audio(duration=config.DURATION, sample_rate=config.SAMPLE_RATE):
        """
        Records audio from the microphone and returns it as a numpy array.
        """
        print(f"\n🎤 Recording for {duration} seconds...")
        audio = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype='int16'
        )
        sd.wait()
        print("✅ Recording complete")
        return audio

    @staticmethod
    def save_audio(audio, filename=config.TEMP_AUDIO_FILE, sample_rate=config.SAMPLE_RATE):
        """
        Saves audio numpy array to a WAV file.
        """
        wav.write(filename, sample_rate, audio)
        # print(f"DEBUG: Audio saved to {filename}")
