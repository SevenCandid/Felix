import pyttsx3

engine = pyttsx3.init()

# Optional: adjust voice settings
engine.setProperty('rate', 170)   # speed
engine.setProperty('volume', 1.0) # volume

# Get available voices
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # try 0 or 1

while True:
    text = input("\nType something for Felix to say: ")

    if text.lower() == "exit":
        break

    print("🔊 Felix speaking...")
    engine.say(text)
    engine.runAndWait()