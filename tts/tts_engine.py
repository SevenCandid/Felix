import pyttsx3
from gtts import gTTS
import os
from core.config import TTS_RATE, TTS_VOLUME, TTS_VOICE_INDEX, TTS_MODE

class TTSEngine:
    def __init__(self):
        self.mode = TTS_MODE
        if self.mode == "local":
            self.engine = pyttsx3.init()
            self.setup_local()
        else:
            print("TTS: Using Google Cloud Mode")

    def setup_local(self):
        voices = self.engine.getProperty('voices')
        if TTS_VOICE_INDEX < len(voices):
            self.engine.setProperty('voice', voices[TTS_VOICE_INDEX].id)
        self.engine.setProperty('rate', TTS_RATE)
        self.engine.setProperty('volume', TTS_VOLUME)

    def speak(self, text):
        if self.mode == "local":
            self.engine.say(text)
            self.engine.runAndWait()
        else:
            # For cloud mode, 'speak' isn't used as much as 'save_to_file' for the web
            print(f"Felix says: {text}")

    def save_to_file(self, text, filename="output.mp3"):
        """Saves text to audio file for web serving"""
        try:
            if self.mode == "google":
                # Use gTTS (Cloud)
                tts = gTTS(text=text, lang='en')
                tts.save(filename)
                return True
            else:
                # Use pyttsx3 (Local)
                # Note: pyttsx3 save_to_file usually requires .wav on some systems
                # We'll try to save it as the requested filename
                self.engine.save_to_file(text, filename)
                self.engine.runAndWait()
                return True
        except Exception as e:
            print(f"TTS Error: {e}")
            return False
