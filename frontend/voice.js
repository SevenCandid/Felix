class VoiceHandler {
    constructor() {
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.currentAudio = null; // Track playing audio for interruption
        
        // Visualizer & Silence Detection
        this.audioCtx = null;
        this.analyser = null;
        this.dataArray = null;
        this.animationId = null;
        this.canvas = document.getElementById("waveform");
        this.canvasCtx = this.canvas ? this.canvas.getContext("2d") : null;
        this.waveformContainer = document.getElementById("waveform-container");
        
        // Silence detection thresholds
        this.silenceThreshold = 10; // Adjust based on mic sensitivity
        this.silenceDuration = 1500; // ms of silence before auto-stop
        this.lastAudibleTime = null;
    }

    async startRecording(onStopCallback) {
        try {
            // Interrupt any current playback
            this.stopPlayback();

            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.mediaRecorder = new MediaRecorder(stream);
            this.audioChunks = [];

            // Initialize Visualizer and Silence Detection
            this.initVisualizer(stream, onStopCallback);

            this.mediaRecorder.ondataavailable = (event) => {
                this.audioChunks.push(event.data);
            };

            this.mediaRecorder.onstop = () => {
                const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
                onStopCallback(audioBlob);
                
                this.stopVisualizer();
                stream.getTracks().forEach(track => track.stop());
            };

            this.mediaRecorder.start();
            this.isRecording = true;
            this.lastAudibleTime = Date.now();
            return true;
        } catch (error) {
            console.error("Microphone access denied:", error);
            alert("Please allow microphone access to use voice input.");
            return false;
        }
    }

    initVisualizer(stream, onStopCallback) {
        if (!this.canvasCtx) return;

        this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const source = this.audioCtx.createMediaStreamSource(stream);
        this.analyser = this.audioCtx.createAnalyser();
        this.analyser.fftSize = 256;
        source.connect(this.analyser);

        const bufferLength = this.analyser.frequencyBinCount;
        this.dataArray = new Uint8Array(bufferLength);

        this.waveformContainer.classList.add("active");
        this.draw(onStopCallback);
    }

    draw(onStopCallback) {
        if (!this.isRecording) return;
        
        this.animationId = requestAnimationFrame(() => this.draw(onStopCallback));
        this.analyser.getByteFrequencyData(this.dataArray);

        // Calculate average volume for silence detection
        let sum = 0;
        for (let i = 0; i < this.dataArray.length; i++) {
            sum += this.dataArray[i];
        }
        const average = sum / this.dataArray.length;

        if (average > this.silenceThreshold) {
            this.lastAudibleTime = Date.now();
        } else if (Date.now() - this.lastAudibleTime > this.silenceDuration) {
            // Auto-stop recording after silence
            this.stopRecording();
            return;
        }

        const width = this.canvas.width;
        const height = this.canvas.height;
        this.canvasCtx.clearRect(0, 0, width, height);

        const barWidth = (width / this.dataArray.length) * 2.5;
        let x = 0;

        for (let i = 0; i < this.dataArray.length; i++) {
            const barHeight = (this.dataArray[i] / 255) * height;
            const gradient = this.canvasCtx.createLinearGradient(0, height, 0, 0);
            gradient.addColorStop(0, '#4285f4');
            gradient.addColorStop(1, '#c6a7ff');

            this.canvasCtx.fillStyle = gradient;
            this.canvasCtx.fillRect(x, height - barHeight, barWidth, barHeight);
            x += barWidth + 1;
        }
    }

    stopVisualizer() {
        this.isRecording = false;
        if (this.animationId) cancelAnimationFrame(this.animationId);
        if (this.audioCtx) this.audioCtx.close();
        if (this.waveformContainer) this.waveformContainer.classList.remove("active");
    }

    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.isRecording = false;
        }
    }

    playAudio(url) {
        if (!url) return;
        this.stopPlayback(); // Stop any previous audio
        this.currentAudio = new Audio(url);
        this.currentAudio.play();
    }

    stopPlayback() {
        if (this.currentAudio) {
            this.currentAudio.pause();
            this.currentAudio.currentTime = 0;
            this.currentAudio = null;
        }
    }

    get isPlaying() {
        return this.currentAudio && !this.currentAudio.paused;
    }
}

const Voice = new VoiceHandler();
