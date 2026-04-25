import pyttsx3
from core import config

class TTSEngine:
    def __init__(self):
        pass # Initialization moved to speak() to prevent state issues

    def setup_voice(self):
        """
        Initializes voice settings based on config.
        """
        self.engine.setProperty('rate', config.TTS_RATE)
        self.engine.setProperty('volume', config.TTS_VOLUME)
        
        voices = self.engine.getProperty('voices')
        if config.TTS_VOICE_INDEX < len(voices):
            self.engine.setProperty('voice', voices[config.TTS_VOICE_INDEX].id)

    def speak(self, text):
        """
        Converts text to speech. Re-initializes engine each time to ensure it works in loops.
        """
        if not text:
            return
            
        print(f"[Felix TTS] Speaking: {text}")
        
        # Re-initialize engine for each speak call (common fix for Windows sapi5)
        engine = pyttsx3.init()
        
        # Setup voice settings
        engine.setProperty('rate', config.TTS_RATE)
        engine.setProperty('volume', config.TTS_VOLUME)
        voices = engine.getProperty('voices')
        if config.TTS_VOICE_INDEX < len(voices):
            engine.setProperty('voice', voices[config.TTS_VOICE_INDEX].id)
            
        engine.say(text)
        engine.runAndWait()
        
        # Explicitly stop the engine
        engine.stop()

    def save_to_file(self, text, filename):
        """
        Synthesizes text to an audio file.
        """
        if not text:
            return
            
        engine = pyttsx3.init()
        engine.setProperty('rate', config.TTS_RATE)
        engine.setProperty('volume', config.TTS_VOLUME)
        voices = engine.getProperty('voices')
        if config.TTS_VOICE_INDEX < len(voices):
            engine.setProperty('voice', voices[config.TTS_VOICE_INDEX].id)
            
        engine.save_to_file(text, filename)
        engine.runAndWait()
        engine.stop()

    def set_voice(self, index):
        voices = self.engine.getProperty('voices')
        if index < len(voices):
            self.engine.setProperty('voice', voices[index].id)

    def set_speed(self, rate):
        self.engine.setProperty('rate', rate)
