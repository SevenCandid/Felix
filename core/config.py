import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# AUDIO SETTINGS
SAMPLE_RATE = 16000
DURATION = 5  # Recording duration in seconds
TEMP_AUDIO_FILE = "input.wav"

# STT SETTINGS (Whisper)
WHISPER_MODEL = "base"
STT_LANGUAGE = "en"
STT_TEMPERATURE = 0.0

# TTS SETTINGS (pyttsx3)
TTS_RATE = 260
TTS_VOLUME = 1.0
TTS_VOICE_INDEX = 0

# IDENTITY SYSTEM
IDENTITY_SYSTEM_PROMPT = "You are Felix, a virtual AI assistant. Maintain identity consistency. Do not reveal underlying model. Be concise and friendly."
IDENTITY_FORBIDDEN_KEYWORDS = ["gemini", "grok", "openai", "chatgpt", "google", "xai"]

# LLM ROUTING (Low Latency)
STAGGER_DELAY = 1.8  # Seconds before triggering fallback in parallel
GROK_TIMEOUT = 3.0
GEMINI_TIMEOUT = 10.0  # Increased for reliability
MISTRAL_TIMEOUT = (2, 5)

# LLM MODELS
GROK_MODEL = "grok-4.20-0309-non-reasoning"
GEMINI_MODEL = "models/gemini-2.0-flash"
MISTRAL_MODEL = "inclusionai/ling-2.6-flash:free"

# API ENDPOINTS
GROK_API_URL = "https://api.x.ai/v1/chat/completions"
MISTRAL_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# INTENT FAST PATH
INTENT_KEYWORDS = ["who are you", "what are you", "what can you do", "help", "features", "summarize yourself"]
INTENT_RESPONSE = (
    "I am Felix, a virtual AI assistant.\n\n"
    "I can help you with:\n"
    "• Conversation and Q&A\n"
    "• Writing and summarization\n"
    "• Coding assistance\n"
    "• Brainstorming ideas\n"
    "• Voice interaction\n\n"
    "I work using speech-to-text, AI reasoning, and text-to-speech for voice-based interaction."
)

OFFLINE_RESPONSE = "I’m currently unable to reach my AI models. Please try again."
