import os
import time
from stt.whisper_engine import WhisperEngine
from tts.tts_engine import TTSEngine
from llm.router import HybridRouter
from core import config

def verify_phase1():
    print("[PHASE 1 VERIFY] Starting Phase 1 Verification...")
    
    # 1. Test TTS (Google Mode)
    print("\n[PHASE 1 VERIFY] Testing Google TTS...")
    tts = TTSEngine()
    test_text = "Hello, I am Felix. Phase one verification is in progress."
    test_file = "test_voice.mp3"
    
    if os.path.exists(test_file):
        os.remove(test_file)
        
    success = tts.save_to_file(test_text, test_file)
    if success and os.path.exists(test_file):
        print(f"[PHASE 1 VERIFY] SUCCESS: Created {test_file} ({os.path.getsize(test_file)} bytes)")
    else:
        print("[PHASE 1 VERIFY] FAILED: Google TTS")

    # 2. Test STT (Tiny Whisper)
    print("\n[PHASE 1 VERIFY] Testing Tiny Whisper...")
    stt = WhisperEngine(model_name="tiny")
    print("[PHASE 1 VERIFY] SUCCESS: Tiny Whisper model loaded.")

    # 3. Test LLM Router
    print("\n[PHASE 1 VERIFY] Testing LLM Router...")
    router = HybridRouter()
    try:
        response = router.send_to_llm("Say 'Phase 1 Verified'", model_choice="gemini")
        print(f"[PHASE 1 VERIFY] SUCCESS: LLM Response: {response}")
    except Exception as e:
        print(f"[PHASE 1 VERIFY] FAILED: LLM connectivity: {e}")

    print("\n[PHASE 1 VERIFY] Verification Complete!")

if __name__ == "__main__":
    verify_phase1()
