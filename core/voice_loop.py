import sys
from core.controller import FelixController

class VoiceLoop:
    def __init__(self):
        self.controller = FelixController()

    def start(self):
        """
        Runs the main voice loop.
        """
        print("Welcome! I am Felix, your AI voice assistant.")
        print("Press Ctrl+C to exit at any time.")
        
        try:
            while True:
                input("\n>>> Press ENTER to start recording...")
                self.controller.process_voice_input()
        except KeyboardInterrupt:
            print("\n\nExiting Felix. Goodbye!")
            sys.exit(0)
