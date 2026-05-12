/**
 * JARVIS PRIME - UI Logic
 * Connects via WebSocket to the Python Daemon.
 */

const wsUrl = "ws://localhost:9999/ws";
let ws = null;
let isSimulationMode = false; // Set to true when deploying to Vercel/Netlify for portfolios

// Elements
const statusIndicator = document.getElementById('connection-status');
const chatFeed = document.getElementById('chat-feed');
const cmdInput = document.getElementById('cmd-input');
const sendBtn = document.getElementById('send-btn');
const cpuBar = document.getElementById('cpu-bar');
const cpuText = document.getElementById('cpu-text');
const ramBar = document.getElementById('ram-bar');
const ramText = document.getElementById('ram-text');
const visualizer = document.getElementById('audio-visualizer');

// Clock Update
setInterval(() => {
    document.getElementById('sys-clock').innerText = new Date().toLocaleTimeString('en-US', { hour12: false });
}, 1000);

// Initialize
function init() {
    if (window.location.hostname !== "localhost" && window.location.hostname !== "127.0.0.1") {
        isSimulationMode = true;
        appendMessage("system", "Running in Portfolio Simulation Mode. Core disconnected.");
        setStatus(true); // Fake online
    } else {
        connectWebSocket();
    }
}

function setStatus(online) {
    if (online) {
        statusIndicator.classList.add('online');
    } else {
        statusIndicator.classList.remove('online');
    }
}

function connectWebSocket() {
    ws = new WebSocket(wsUrl);

    ws.onopen = () => {
        setStatus(true);
        appendMessage("system", "Core Link Established. Awaiting Input.");
        sendSystemCheck(); // Auto-fetch stats on boot
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        hideVisualizer();
        
        if (data.intent === "system_status") {
            // Parse fake telemetry if it's just text for now, but we'll show the text.
            // A real system would send structured JSON for CPU/RAM.
            appendMessage("prime", data.response);
            
            // Temporary dummy visual update based on string
            const cpuMatch = data.response.match(/CPU at ([\d.]+)%/);
            const ramMatch = data.response.match(/Memory at ([\d.]+)%/);
            if (cpuMatch) updateStats('cpu', parseFloat(cpuMatch[1]));
            if (ramMatch) updateStats('ram', parseFloat(ramMatch[1]));
            
        } else {
            appendMessage("prime", data.response);
        }
    };

    ws.onclose = () => {
        setStatus(false);
        appendMessage("system", "Core Link Lost. Attempting reconnect in 5s...");
        setTimeout(connectWebSocket, 5000);
    };

    ws.onerror = (err) => {
        console.error("WebSocket Error:", err);
        ws.close();
    };
}

function sendCommand() {
    const text = cmdInput.value.trim();
    if (!text) return;

    appendMessage("user", text);
    cmdInput.value = "";
    showVisualizer();

    if (isSimulationMode) {
        setTimeout(() => {
            hideVisualizer();
            appendMessage("prime", `Simulation Mode Active. Executing vector: ${text}`);
        }, 1500);
        return;
    }

    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ command: text }));
    } else {
        hideVisualizer();
        appendMessage("system", "Cannot send. Core is offline.");
    }
}

function sendSystemCheck() {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ command: "system status" }));
        showVisualizer();
    }
}

function updateStats(type, percent) {
    if (type === 'cpu') {
        cpuBar.style.width = `${percent}%`;
        cpuText.innerText = `${percent.toFixed(1)}%`;
        cpuBar.className = `progress-bar progress-bar-striped progress-bar-animated ${percent > 80 ? 'bg-danger' : 'bg-cyan'}`;
    } else if (type === 'ram') {
        ramBar.style.width = `${percent}%`;
        ramText.innerText = `${percent.toFixed(1)}%`;
        ramBar.className = `progress-bar progress-bar-striped progress-bar-animated ${percent > 80 ? 'bg-danger' : 'bg-blue'}`;
    }
}

function appendMessage(sender, text) {
    const div = document.createElement('div');
    div.className = `msg ${sender}-msg`;
    
    let icon = "";
    if (sender === "user") icon = '<i class="fa-solid fa-user me-2 text-blue"></i>';
    if (sender === "prime") icon = '<i class="fa-solid fa-robot me-2 text-cyan"></i>';
    
    div.innerHTML = `${icon}${text}`;
    chatFeed.appendChild(div);
    chatFeed.scrollTop = chatFeed.scrollHeight;
}

function showVisualizer() {
    visualizer.classList.remove('d-none');
}

function hideVisualizer() {
    visualizer.classList.add('d-none');
}

// Event Listeners
sendBtn.addEventListener('click', sendCommand);
cmdInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendCommand();
});

// Boot
init();
