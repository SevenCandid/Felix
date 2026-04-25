import os
import requests
from core import config

class GrokClient:
    def __init__(self):
        self.api_key = os.getenv("XAI_API_KEY")
        self.url = config.GROK_API_URL
        self.model = config.GROK_MODEL

    def send_to_llm(self, text, timeout=config.GROK_TIMEOUT):
        """
        Sends text to Grok with Felix identity injection.
        """
        if not self.api_key:
            raise Exception("XAI_API_KEY not found")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
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
                raise Exception(f"Grok API Error {response.status_code}")

        except Exception as e:
            raise Exception(str(e))

    def _sanitize_response(self, text):
        """
        Ensures the response doesn't contain forbidden keywords.
        """
        lower_text = text.lower()
        for word in config.IDENTITY_FORBIDDEN_KEYWORDS:
            if word in lower_text:
                # If identity leak detected, return generic Felix response
                return "I am Felix, your virtual AI assistant. How can I help you today?"
        return text
