import whisper
from core import config

class WhisperEngine:
    def __init__(self, model_name=config.WHISPER_MODEL):
        print(f"Loading Whisper model '{model_name}'...")
        self.model = whisper.load_model(model_name)
        print("Whisper model loaded.")

    def transcribe(self, audio_file):
        """
        Transcribes the given audio file using Whisper.
        """
        print(f"[Felix STT] Transcribing {audio_file}...")
        result = self.model.transcribe(
            audio_file,
            language=config.STT_LANGUAGE,
            temperature=config.STT_TEMPERATURE
        )
        text = result.get("text", "").strip()
        return text
