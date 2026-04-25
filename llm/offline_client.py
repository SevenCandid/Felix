from core import config

class OfflineClient:
    def __init__(self):
        pass

    def send_to_llm(self, text):
        """
        Returns a hardcoded offline response.
        Can be extended later with a local model like Mistral 7B.
        """
        # print("[Felix LLM] Using Offline Mode")
        return config.OFFLINE_RESPONSE
