import os
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from llm.router import HybridRouter
from stt.whisper_engine import WhisperEngine
from tts.tts_engine import TTSEngine
from core import config

app = Flask(__name__, static_folder='frontend')
CORS(app)

# Initialize engines
router = HybridRouter()
stt_engine = WhisperEngine()
tts_engine = TTSEngine()

# Ensure temp directory exists
TEMP_DIR = "temp"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        text = data.get('text', '')
        model = data.get('model', 'auto')
        
        print(f"[Server] Received chat request: {text} (Model: {model})")
        
        response = router.send_to_llm(text, model_choice=model)
        return jsonify({"response": response})
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        print(f"[Server Error] {error_msg}")
        return jsonify({"response": f"Internal Server Error: {str(e)}"}), 500

@app.route('/stt', methods=['POST'])
def stt():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file"}), 400
    
    audio_file = request.files['audio']
    audio_path = os.path.join(TEMP_DIR, "web_input.wav")
    audio_file.save(audio_path)
    
    print(f"[Server] Received audio for transcription")
    text = stt_engine.transcribe(audio_path)
    return jsonify({"text": text})

@app.route('/tts', methods=['POST'])
def tts():
    data = request.json
    text = data.get('text', '')
    
    output_path = os.path.join(TEMP_DIR, "web_output.mp3") # pyttsx3 usually saves as wav or mp3 depending on OS
    if os.path.exists(output_path):
        os.remove(output_path)
        
    print(f"[Server] Synthesizing text to speech: {text}")
    tts_engine.save_to_file(text, output_path)
    
    # Wait for file to be ready (pyttsx3 is synchronous but sometimes filesystem lags)
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    print("🚀 Felix Web Server starting at http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
