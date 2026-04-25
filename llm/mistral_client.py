import os
import requests
from core import config

class MistralClient:
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.url = config.MISTRAL_API_URL
        self.model = config.MISTRAL_MODEL

    def send_to_llm(self, text, timeout=config.MISTRAL_TIMEOUT):
        """
        Sends text to Mistral (via OpenRouter) with a strict timeout.
        """
        if not self.api_key:
            raise Exception("MISTRAL_API_KEY not found")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/felix-assistant",
            "X-Title": "Felix AI Assistant"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": config.IDENTITY_SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ],
            "temperature": 0.7
        }

        try:
            response = requests.post(
                self.url,
                headers=headers,
                json=payload,
                timeout=timeout
            )

            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                return self._sanitize_response(content)
            else:
                raise Exception(f"API Error {response.status_code}")

        except Exception as e:
            raise Exception(str(e))

    def _sanitize_response(self, text):
        lower_text = text.lower()
        for word in config.IDENTITY_FORBIDDEN_KEYWORDS:
            if word in lower_text:
                return "I am Felix, your virtual AI assistant. How can I help you today?"
        return text
