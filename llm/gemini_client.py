import os
import google.generativeai as genai
from core import config

class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.model_name = config.GEMINI_MODEL
        self.model = None
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(
                    model_name=self.model_name,
                    system_instruction=config.IDENTITY_SYSTEM_PROMPT
                )
            except Exception:
                pass

    def send_to_llm(self, text, timeout=config.GEMINI_TIMEOUT):
        """
        Sends text to Gemini with Felix identity injection.
        """
        if not self.model:
            raise Exception("Gemini not configured")

        response = self.model.generate_content(
            text, 
            request_options={"timeout": timeout}
        )
        
        if response and response.text:
            content = response.text.strip()
            return self._sanitize_response(content)
        else:
            raise Exception("Empty Gemini response")

    def _sanitize_response(self, text):
        lower_text = text.lower()
        for word in config.IDENTITY_FORBIDDEN_KEYWORDS:
            if word in lower_text:
                return "I am Felix, your virtual AI assistant. How can I help you today?"
        return text
