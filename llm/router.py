import threading
import time
import queue
from llm.grok_client import GrokClient
from llm.gemini_client import GeminiClient
from llm.mistral_client import MistralClient
from llm.offline_client import OfflineClient
from core import config

class HybridRouter:
    def __init__(self):
        self.grok = GrokClient()
        self.gemini = GeminiClient()
        self.mistral = MistralClient()
        self.offline = OfflineClient()
        self.result_queue = queue.Queue()

    def send_to_llm(self, text, model_choice="auto"):
        """
        Routes the request based on choice:
        - auto: Staggered Parallel Race
        - grok/gemini/mistral: Forced model selection
        """
        print(f"[Felix Router] Input received (Choice: {model_choice})")
        
        # Handle forced model selection
        if model_choice == "grok":
            return self.grok.send_to_llm(text)
        elif model_choice == "gemini":
            return self.gemini.send_to_llm(text)
        elif model_choice == "mistral":
            return self.mistral.send_to_llm(text)
        
        # Default: Staggered Parallel Race
        
        # Reset queue for this request
        self.result_queue = queue.Queue()
        
        # Thread for Grok
        grok_thread = threading.Thread(target=self._call_grok, args=(text,))
        grok_thread.daemon = True
        grok_thread.start()
        
        start_time = time.time()
        
        # Staggered wait
        while time.time() - start_time < config.STAGGER_DELAY:
            try:
                # Check if Grok finished early
                source, response = self.result_queue.get(timeout=0.1)
                duration = round(time.time() - start_time, 2)
                print(f"[Felix Router] {source} responded in {duration}s")
                return response
            except queue.Empty:
                continue
                
        # If we reach here, Grok is taking too long
        print("[Felix Router] Grok slow → triggering Gemini early")
        
        # Thread for Gemini
        gemini_thread = threading.Thread(target=self._call_gemini, args=(text,))
        gemini_thread.daemon = True
        gemini_thread.start()
        
        # Race!
        max_total_wait = max(config.GROK_TIMEOUT, config.GEMINI_TIMEOUT)
        
        while time.time() - start_time < max_total_wait + 0.5:
            try:
                source, response = self.result_queue.get(timeout=0.5)
                duration = round(time.time() - start_time, 2)
                print(f"[Felix Router] {source} responded in {duration}s")
                print(f"[Felix Router] Final response selected")
                return response
            except queue.Empty:
                if not grok_thread.is_alive() and not gemini_thread.is_alive():
                    break
                continue

        # If both fail, try Mistral as a sequential fallback
        print("[Felix Router] Grok and Gemini failed → trying Mistral fallback")
        try:
            start_mistral = time.time()
            response = self.mistral.send_to_llm(text)
            duration = round(time.time() - start_mistral, 2)
            print(f"[Felix Router] Mistral responded in {duration}s")
            return response
        except Exception as e:
            print(f"[Felix Router] Mistral failed: {e}")

        print("[Felix Router] All cloud APIs failed")
        return config.OFFLINE_RESPONSE

    def _call_grok(self, text):
        try:
            print("[Felix Router] Grok requested")
            response = self.grok.send_to_llm(text)
            self.result_queue.put(("Grok", response))
        except Exception as e:
            print(f"[Felix Router] DEBUG: Grok error: {e}")
            pass

    def _call_gemini(self, text):
        try:
            print("[Felix Router] Gemini requested")
            response = self.gemini.send_to_llm(text)
            self.result_queue.put(("Gemini", response))
        except Exception as e:
            print(f"[Felix Router] DEBUG: Gemini error: {e}")
            pass
