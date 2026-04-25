const Voice = {
    recognition: null,
    isRecording: false,
    isPlaying: false,
    audioElement: null,

    init() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SpeechRecognition) {
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';
        } else {
            console.warn("Browser does not support Speech Recognition.");
        }
    },

    async startRecording(onResult) {
        if (!this.recognition) {
            alert("Speech recognition is not supported in this browser. Please use Chrome or Edge.");
            return false;
        }

        return new Promise((resolve) => {
            this.recognition.onstart = () => {
                this.isRecording = true;
                resolve(true);
            };

            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                this.isRecording = false;
                onResult({ text: transcript });
            };

            this.recognition.onerror = (event) => {
                console.error("Speech Recognition Error:", event.error);
                this.isRecording = false;
                onResult({ text: "" });
            };

            this.recognition.onend = () => {
                this.isRecording = false;
            };

            this.recognition.start();
        });
    },

    stopRecording() {
        if (this.recognition && this.isRecording) {
            this.recognition.stop();
            this.isRecording = false;
        }
    },

    playAudio(url) {
        if (this.audioElement) {
            this.audioElement.pause();
        }
        this.audioElement = new Audio(url);
        this.isPlaying = true;
        this.audioElement.onended = () => { this.isPlaying = false; };
        this.audioElement.play();
    },

    stopPlayback() {
        if (this.audioElement) {
            this.audioElement.pause();
            this.isPlaying = false;
        }
    }
};

// Initialize on load
Voice.init();
