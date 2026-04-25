const chatMessages = document.getElementById("chat-messages");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const micBtn = document.getElementById("mic-btn");
const modelSelector = document.getElementById("model-selector");
const ttsToggle = document.getElementById("tts-toggle");
const statusIndicator = document.getElementById("status");
const latencyIndicator = document.getElementById("latency-indicator");
const welcomeScreen = document.getElementById("welcome-screen");
const pulseWave = document.getElementById("pulse-wave");
const chips = document.querySelectorAll(".chip");

// Configure Markdown with custom renderer for Copy Button
const renderer = new marked.Renderer();
renderer.code = function(code, lang) {
    const validLang = !!(lang && hljs.getLanguage(lang));
    const highlighted = validLang ? hljs.highlight(code, { language: lang }).value : hljs.highlightAuto(code).value;
    return `
        <div class="code-block-wrapper">
            <button class="copy-btn" onclick="copyToClipboard(this)">COPY</button>
            <pre><code class="hljs ${lang}">${highlighted}</code></pre>
        </div>
    `;
};
marked.setOptions({ renderer, breaks: true });

// Auto-resize textarea
userInput.addEventListener("input", () => {
    userInput.style.height = "auto";
    userInput.style.height = (userInput.scrollHeight) + "px";
});

// Send message on Enter
userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleSend();
    }
});

sendBtn.addEventListener("click", handleSend);

// Handle Suggestion Chips
chips.forEach(chip => {
    chip.addEventListener("click", () => {
        const query = chip.getAttribute("data-query");
        userInput.value = query;
        handleSend();
    });
});

async function handleSend() {
    const text = userInput.value.trim();
    if (!text) return;

    if (welcomeScreen) welcomeScreen.style.display = "none";

    userInput.value = "";
    userInput.style.height = "auto";
    
    appendMessage("user", text);
    const thinkingId = appendThinking();
    
    statusIndicator.innerText = "Thinking...";
    const startTime = Date.now();
    
    const selectedModel = modelSelector.value;
    const data = await API.chat(text, selectedModel);
    
    const latency = ((Date.now() - startTime) / 1000).toFixed(1);
    latencyIndicator.innerText = `${latency}s`;
    
    removeElement(thinkingId);
    
    // Use simulated streaming
    await appendMessageStreamed("felix", data.response);
    
    statusIndicator.innerText = "Ready";
    
    if (ttsToggle.checked) {
        const audioUrl = await API.synthesize(data.response);
        if (audioUrl) Voice.playAudio(audioUrl);
    }

    // Show follow-up chips
    showFollowUps();
}

// Voice Recording Logic
micBtn.addEventListener("click", async () => {
    if (Voice.isPlaying) Voice.stopPlayback();

    if (Voice.isRecording) {
        Voice.stopRecording();
        micBtn.classList.remove("active");
        statusIndicator.innerText = "Transcribing...";
        return;
    }

    // Trigger Pulse Wave
    pulseWave.classList.add("active");
    setTimeout(() => pulseWave.classList.remove("active"), 1500);

    const started = await Voice.startRecording(async (data) => {
        micBtn.classList.remove("active");
        
        if (data.text) {
            userInput.value = data.text;
            handleSend();
        } else {
            statusIndicator.innerText = "Ready";
        }
    });
    
    if (started) {
        micBtn.classList.add("active");
        statusIndicator.innerText = "Listening...";
    }
});

// UI Helpers
function appendMessage(role, text) {
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${role}-message`;
    const avatar = role === "user" ? "" : '<div class="avatar"><div class="felix-orb"></div></div>';
    msgDiv.innerHTML = `${avatar}<div class="message-content">${text}</div>`;
    chatMessages.appendChild(msgDiv);
    scrollToBottom();
}

async function appendMessageStreamed(role, text) {
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${role}-message`;
    const avatar = '<div class="avatar"><div class="felix-orb"></div></div>';
    
    msgDiv.innerHTML = `${avatar}<div class="message-content"></div>`;
    chatMessages.appendChild(msgDiv);
    const contentDiv = msgDiv.querySelector(".message-content");
    
    const words = text.split(" ");
    let currentText = "";
    
    for (let i = 0; i < words.length; i++) {
        currentText += words[i] + " ";
        contentDiv.innerHTML = marked.parse(currentText);
        scrollToBottom();
        await new Promise(resolve => setTimeout(resolve, 20 + Math.random() * 30));
    }
}

function showFollowUps() {
    // Remove existing follow-ups
    const oldContainer = document.querySelector(".follow-up-container");
    if (oldContainer) oldContainer.remove();

    const container = document.createElement("div");
    container.className = "follow-up-container";
    
    const suggestions = ["Tell me more", "Simplify that", "Give me an example"];
    suggestions.forEach(text => {
        const btn = document.createElement("button");
        btn.className = "mini-chip";
        btn.innerText = text;
        btn.onclick = () => {
            userInput.value = text;
            handleSend();
        };
        container.appendChild(btn);
    });
    
    chatMessages.appendChild(container);
    scrollToBottom();
}

function appendThinking() {
    const id = "thinking-" + Date.now();
    const thinkingDiv = document.createElement("div");
    thinkingDiv.id = id;
    thinkingDiv.className = "message felix-message";
    thinkingDiv.innerHTML = `
        <div class="avatar">
            <div class="felix-orb thinking"></div>
            <div class="particles">
                <div class="particle p1"></div>
                <div class="particle p2"></div>
                <div class="particle p3"></div>
            </div>
        </div>
        <div class="message-content">
            <div class="thinking">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        </div>
    `;
    chatMessages.appendChild(thinkingDiv);
    scrollToBottom();
    return id;
}

function copyToClipboard(btn) {
    const code = btn.nextElementSibling.innerText;
    navigator.clipboard.writeText(code);
    btn.innerText = "COPIED!";
    btn.style.color = "var(--accent-violet)";
    setTimeout(() => {
        btn.innerText = "COPY";
        btn.style.color = "var(--text-secondary)";
    }, 2000);
}

function removeElement(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Initial canvas sizing
window.addEventListener('resize', () => {
    if (Voice.canvas) {
        Voice.canvas.width = Voice.canvas.offsetWidth;
        Voice.canvas.height = Voice.canvas.offsetHeight;
    }
});
setTimeout(() => {
    if (Voice.canvas) {
        Voice.canvas.width = Voice.canvas.offsetWidth;
        Voice.canvas.height = Voice.canvas.offsetHeight;
    }
}, 100);
