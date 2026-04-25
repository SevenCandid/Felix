import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def diagnostic_gemini():
    print("\n--- Gemini Diagnostic ---")
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("GOOGLE_API_KEY not found.")
        return
    try:
        genai.configure(api_key=api_key)
        print("Available Gemini models:")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"Gemini error: {e}")

def diagnostic_openrouter():
    print("\n--- OpenRouter Diagnostic ---")
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        print("MISTRAL_API_KEY not found.")
        return
    url = "https://openrouter.ai/api/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            models = response.json().get("data", [])
            print(f"Top 5 OpenRouter models:")
            for m in models[:10]:
                print(f"- {m['id']}")
        else:
            print(f"OpenRouter error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"OpenRouter network error: {e}")

if __name__ == "__main__":
    diagnostic_gemini()
    diagnostic_openrouter()
