import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

# SETTINGS
DURATION = 5  # recording time in seconds
SAMPLE_RATE = 16000

print("Loading Whisper model...")
model = whisper.load_model("small")  # you can change to "small" later

def record_audio():
    print("\n🎤 Speak now...")
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()
    print("✅ Recording complete")
    return audio

def save_audio(audio, filename="input.wav"):
    wav.write(filename, SAMPLE_RATE, audio)

def transcribe_audio(filename="input.wav"):
    print("🧠 Transcribing...")
    result = model.transcribe(
        filename,
        language="en",
        temperature=0.0  # reduces randomness
    )
    return result["text"]

# MAIN LOOP
while True:
    input("\nPress ENTER to start recording...")
    
    audio = record_audio()
    save_audio(audio)
    
    text = transcribe_audio()
    
    print(f"\n📝 You said: {text}")