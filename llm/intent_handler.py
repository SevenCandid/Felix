from core import config

class IntentHandler:
    @staticmethod
    def check_intent(text):
        """
        Checks if the user input matches any predefined intents.
        Returns a fixed response if matched, otherwise None.
        """
        if not text:
            return None
            
        clean_text = text.lower().strip().replace("?", "")
        
        for keyword in config.INTENT_KEYWORDS:
            if keyword in clean_text:
                print(f"[Felix Router] Intent detected: {keyword}")
                return config.INTENT_RESPONSE
                
        return None
