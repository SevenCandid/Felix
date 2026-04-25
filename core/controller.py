from stt.whisper_engine import WhisperEngine
from tts.tts_engine import TTSEngine
from llm.router import HybridRouter
from llm.intent_handler import IntentHandler
from utils.audio_helper import AudioHelper
from core import config

class FelixController:
    def __init__(self):
        print("\n--- Initializing Felix ---")
        self.stt = WhisperEngine()
        self.tts = TTSEngine()
        self.router = HybridRouter()
        self.intent_handler = IntentHandler()
        print("--- Felix is Ready ---\n")

    def process_voice_input(self):
        """
        Executes one full cycle: Record -> Transcribe -> Intent -> Router -> Speak
        """
        # 1. Record
        audio = AudioHelper.record_audio()
        AudioHelper.save_audio(audio)

        # 2. Transcribe (STT)
        user_text = self.stt.transcribe(config.TEMP_AUDIO_FILE)
        
        if not user_text:
            print("[Felix] I didn't catch that. Please try again.")
            return

        print(f"\n📝 You said: {user_text}")

        # 3. Intent Detection (Fast Path)
        print("[Felix Router] Checking intent")
        response_text = self.intent_handler.check_intent(user_text)
        
        # 4. Hybrid Routing (if no intent matched)
        if not response_text:
            response_text = self.router.send_to_llm(user_text)
            
        print(f"🤖 Felix: {response_text}")

        # 5. Speak (TTS)
        self.tts.speak(response_text)
