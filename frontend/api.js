const API_BASE = ""; // Relative to host when served from same origin

const API = {
    async chat(text, model = "auto") {
        try {
            const response = await fetch(`${API_BASE}/chat`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text, model })
            });
            return await response.json();
        } catch (error) {
            console.error("Chat API Error:", error);
            return { response: "I'm having trouble connecting to my brain. Is the server running?" };
        }
    },

    async transcribe(audioBlob) {
        try {
            const formData = new FormData();
            formData.append("audio", audioBlob, "input.wav");

            const response = await fetch(`${API_BASE}/stt`, {
                method: "POST",
                body: formData
            });
            return await response.json();
        } catch (error) {
            console.error("STT API Error:", error);
            return { text: "" };
        }
    },

    async synthesize(text) {
        try {
            const response = await fetch(`${API_BASE}/tts`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text })
            });
            const blob = await response.blob();
            return URL.createObjectURL(blob);
        } catch (error) {
            console.error("TTS API Error:", error);
            return null;
        }
    }
};
