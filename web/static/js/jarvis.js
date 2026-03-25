/* ═══════════════════════════════════════════════════════
   J.A.R.V.I.S. — Frontend Controller
   Socket.IO + Web Speech API + Particle System
   ═══════════════════════════════════════════════════════ */

// ── Socket.IO Connection ──────────────────────────────
const socket = io();

// ── DOM Elements ──────────────────────────────────────
const chatMessages = document.getElementById('chatMessages');
const commandInput = document.getElementById('commandInput');
const sendBtn = document.getElementById('sendBtn');
const voiceBtn = document.getElementById('voiceBtn');
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const clockEl = document.getElementById('clock');
const dateEl = document.getElementById('dateDisplay');
const toastContainer = document.getElementById('toastContainer');
const activityFeed = document.getElementById('activityFeed');

// ── State ─────────────────────────────────────────────
let isListening = false;
let recognition = null;
let welcomeShown = true;

// ══════════════════════════════════════════════════════
// CLOCK
// ══════════════════════════════════════════════════════
function updateClock() {
    const now = new Date();
    clockEl.textContent = now.toLocaleTimeString('en-US', {
        hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true
    });
    dateEl.textContent = now.toLocaleDateString('en-US', {
        weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
    });
}
updateClock();
setInterval(updateClock, 1000);

// Set boot time
document.getElementById('bootTime').textContent = new Date().toLocaleTimeString('en-US', {
    hour: '2-digit', minute: '2-digit', hour12: false
});

// ══════════════════════════════════════════════════════
// SOCKET EVENTS
// ══════════════════════════════════════════════════════
socket.on('connect', () => {
    setStatus('CONNECTED', 'ready');
    addActivity('Connected to Jarvis server');
});

socket.on('disconnect', () => {
    setStatus('DISCONNECTED', 'error');
    addActivity('Lost connection to server');
});

socket.on('status', (data) => {
    const type = data.type || 'ready';
    setStatus(data.message.toUpperCase(), type);
});

socket.on('response', (data) => {
    removeTyping();
    // Handle special commands
    if (data.text === '__CLEAR_CHAT__') {
        chatMessages.innerHTML = '';
        addActivity('Chat cleared');
        showToast('Chat', 'Chat history cleared', 'info');
        return;
    }
    addMessage(data.text, 'bot', data.timestamp);
    addActivity(`Responded to: "${data.command.substring(0, 30)}..."`);
});

socket.on('system_stats', (data) => {
    updateSystemStats(data);
});

socket.on('notification', (data) => {
    showToast(data.title, data.text, data.type);
    addActivity(`${data.title}: ${data.text.substring(0, 40)}...`);
});

// ══════════════════════════════════════════════════════
// COMMAND HANDLING
// ══════════════════════════════════════════════════════
function sendCommand(text) {
    if (!text || !text.trim()) return;

    // Remove welcome on first message
    if (welcomeShown) {
        const welcome = document.querySelector('.chat-welcome');
        if (welcome) {
            welcome.style.opacity = '0';
            welcome.style.transform = 'translateY(-20px)';
            setTimeout(() => welcome.remove(), 300);
        }
        welcomeShown = false;
    }

    // Add user message
    addMessage(text, 'user');

    // Show typing indicator
    showTyping();

    // Send to server
    socket.emit('command', { text: text });

    // Clear input
    commandInput.value = '';
    commandInput.focus();
}

// Send button
sendBtn.addEventListener('click', () => {
    sendCommand(commandInput.value);
});

// Enter key
commandInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendCommand(commandInput.value);
    }
});

// Quick command buttons
function sendQuick(text) {
    commandInput.value = text;
    sendCommand(text);
}

// ══════════════════════════════════════════════════════
// CHAT UI
// ══════════════════════════════════════════════════════
function addMessage(text, sender, timestamp) {
    const time = timestamp || new Date().toLocaleTimeString('en-US', {
        hour: '2-digit', minute: '2-digit', hour12: true
    });

    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-msg ${sender}`;

    const avatar = sender === 'bot' ? '◈' : '👤';

    // Process text: bold **text** and handle newlines
    let processedText = escapeHtml(text)
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>');

    msgDiv.innerHTML = `
        <div class="msg-avatar">${avatar}</div>
        <div class="msg-bubble">
            <div class="msg-text">${processedText}</div>
            <span class="msg-time">${time}</span>
        </div>
    `;

    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTyping() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'chat-msg bot';
    typingDiv.id = 'typingIndicator';
    typingDiv.innerHTML = `
        <div class="msg-avatar">◈</div>
        <div class="msg-bubble">
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    `;
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTyping() {
    const typing = document.getElementById('typingIndicator');
    if (typing) typing.remove();
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ══════════════════════════════════════════════════════
// STATUS
// ══════════════════════════════════════════════════════
function setStatus(message, type) {
    statusText.textContent = message;
    statusDot.className = 'status-dot';

    if (type === 'processing') {
        statusDot.classList.add('processing');
    } else if (type === 'error') {
        statusDot.classList.add('error');
    }
    // default: green (ready)
}

// ══════════════════════════════════════════════════════
// SYSTEM STATS
// ══════════════════════════════════════════════════════
function updateSystemStats(stats) {
    // CPU (arc reactor)
    const cpuValue = document.getElementById('cpuValue');
    cpuValue.textContent = Math.round(stats.cpu);

    // Adjust reactor glow based on CPU
    const reactor = document.getElementById('arcReactor');
    const intensity = Math.max(0.3, stats.cpu / 100);
    reactor.style.filter = `drop-shadow(0 0 ${10 + stats.cpu * 0.3}px rgba(0, 212, 255, ${intensity}))`;

    // RAM
    document.getElementById('ramFill').style.width = stats.ram + '%';
    document.getElementById('ramValue').textContent = stats.ram + '%';
    document.getElementById('ramUsed').textContent = stats.ram_used + ' / ' + stats.ram_total + ' GB';

    // Disk
    document.getElementById('diskFill').style.width = stats.disk + '%';
    document.getElementById('diskValue').textContent = stats.disk + '%';
    document.getElementById('diskUsed').textContent = stats.disk_used + ' / ' + stats.disk_total + ' GB';

    // Network
    document.getElementById('netValue').textContent = stats.net_recv + ' MB';
    document.getElementById('netRecv').textContent = stats.net_recv + ' MB';
    document.getElementById('netSent').textContent = stats.net_sent + ' MB';

    // Battery
    if (stats.battery !== null) {
        const batteryLevel = document.getElementById('batteryLevel');
        batteryLevel.style.width = stats.battery + '%';

        if (stats.battery > 50) {
            batteryLevel.style.background = 'var(--accent-green)';
        } else if (stats.battery > 20) {
            batteryLevel.style.background = 'var(--accent-orange)';
        } else {
            batteryLevel.style.background = 'var(--accent-red)';
        }

        const plugIcon = stats.plugged ? '⚡' : '🔋';
        document.getElementById('batteryText').textContent = `${plugIcon} ${stats.battery}%`;
    }

    // Color warnings for high usage
    colorGauge('ramFill', stats.ram);
    colorGauge('diskFill', stats.disk);
}

function colorGauge(id, value) {
    const el = document.getElementById(id);
    if (value > 85) {
        el.style.background = 'linear-gradient(90deg, var(--accent-orange), var(--accent-red))';
    } else if (value > 70) {
        el.style.background = 'linear-gradient(90deg, var(--accent-cyan), var(--accent-orange))';
    } else {
        el.style.background = 'linear-gradient(90deg, var(--accent-cyan), var(--accent-blue))';
    }
}

// ══════════════════════════════════════════════════════
// VOICE RECOGNITION (Web Speech API)
// ══════════════════════════════════════════════════════
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onresult = (event) => {
        const text = event.results[0][0].transcript;
        commandInput.value = text;
        sendCommand(text);
        stopListening();
    };

    recognition.onerror = (event) => {
        console.error('Speech error:', event.error);
        stopListening();
        if (event.error !== 'no-speech') {
            showToast('Voice Error', 'Could not recognize speech. Please try again.', 'error');
        }
    };

    recognition.onend = () => {
        stopListening();
    };
}

voiceBtn.addEventListener('click', () => {
    if (isListening) {
        stopListening();
    } else {
        startListening();
    }
});

function startListening() {
    if (!recognition) {
        showToast('Not Supported', 'Voice recognition is not supported in this browser.', 'error');
        return;
    }
    isListening = true;
    voiceBtn.classList.add('active');
    setStatus('LISTENING...', 'processing');
    commandInput.placeholder = '🎤 Listening...';
    try {
        recognition.start();
    } catch(e) {
        // Already started
    }
}

function stopListening() {
    isListening = false;
    voiceBtn.classList.remove('active');
    setStatus('READY', 'ready');
    commandInput.placeholder = 'Ask Jarvis anything...';
    try {
        recognition.stop();
    } catch(e) {}
}

// ══════════════════════════════════════════════════════
// ACTIVITY FEED
// ══════════════════════════════════════════════════════
function addActivity(text) {
    const time = new Date().toLocaleTimeString('en-US', {
        hour: '2-digit', minute: '2-digit', hour12: false
    });

    const item = document.createElement('div');
    item.className = 'activity-item';
    item.innerHTML = `
        <span class="activity-time">${time}</span>
        <span class="activity-text">${escapeHtml(text)}</span>
    `;

    activityFeed.insertBefore(item, activityFeed.firstChild);

    // Limit activity items
    while (activityFeed.children.length > 20) {
        activityFeed.removeChild(activityFeed.lastChild);
    }
}

// ══════════════════════════════════════════════════════
// TOAST NOTIFICATIONS
// ══════════════════════════════════════════════════════
function showToast(title, text, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <div class="toast-title">${escapeHtml(title)}</div>
        <div class="toast-text">${escapeHtml(text)}</div>
    `;
    toastContainer.appendChild(toast);

    // Auto remove after 5 seconds
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(40px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

// ══════════════════════════════════════════════════════
// SLIDE PANELS (Notes, Tasks, Reminders)
// ══════════════════════════════════════════════════════
const overlay = document.getElementById('overlay');

function openPanel(name) {
    closeAllPanels();
    document.getElementById(name + 'Panel').classList.add('active');
    overlay.classList.add('active');
    loadPanelData(name);
}

function closePanel(name) {
    document.getElementById(name + 'Panel').classList.remove('active');
    overlay.classList.remove('active');
}

function closeAllPanels() {
    document.querySelectorAll('.slide-panel').forEach(p => p.classList.remove('active'));
    overlay.classList.remove('active');
}

// ── Notes Panel ───────────────────────────────────────
document.getElementById('noteInput').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        const text = e.target.value.trim();
        if (text) {
            fetch('/api/notes', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({title: text.substring(0, 50), content: text, category: 'general'})
            }).then(() => {
                e.target.value = '';
                loadPanelData('notes');
                addActivity('Note saved');
            });
        }
    }
});

// ── Tasks Panel ───────────────────────────────────────
document.getElementById('taskInput').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        const text = e.target.value.trim();
        const priority = document.getElementById('taskPriority').value;
        if (text) {
            fetch('/api/tasks', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({title: text, priority: priority})
            }).then(() => {
                e.target.value = '';
                loadPanelData('tasks');
                addActivity('Task added');
            });
        }
    }
});

// ── Reminders Panel ───────────────────────────────────
document.getElementById('reminderInput').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        const text = e.target.value.trim();
        const minutes = parseInt(document.getElementById('reminderMinutes').value) || 30;
        if (text) {
            const remindAt = new Date(Date.now() + minutes * 60000).toISOString().slice(0, 19).replace('T', ' ');
            fetch('/api/reminders', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text: text, time: remindAt})
            }).then(() => {
                e.target.value = '';
                loadPanelData('reminders');
                addActivity(`Reminder set: ${text}`);
            });
        }
    }
});

// ── Load Panel Data ───────────────────────────────────
function loadPanelData(name) {
    if (name === 'notes') {
        fetch('/api/notes')
            .then(r => r.json())
            .then(data => {
                const list = document.getElementById('notesList');
                list.innerHTML = '';
                (data.data || []).forEach(note => {
                    list.innerHTML += `
                        <div class="panel-list-item">
                            <div class="item-text">${escapeHtml(note.content)}</div>
                            <div class="item-meta">${note.created_at || ''}</div>
                            <button class="item-delete" onclick="deleteItem('notes', ${note.id})">✕</button>
                        </div>
                    `;
                });
                if (!data.data || data.data.length === 0) {
                    list.innerHTML = '<div style="text-align:center;padding:20px;color:var(--text-dim);">No notes yet</div>';
                }
            });
    } else if (name === 'tasks') {
        fetch('/api/tasks')
            .then(r => r.json())
            .then(data => {
                const list = document.getElementById('tasksList');
                list.innerHTML = '';
                (data.data || []).forEach(task => {
                    const completed = task.is_completed ? 'completed' : '';
                    const checkMark = task.is_completed ? '✓' : '';
                    list.innerHTML += `
                        <div class="panel-list-item ${completed}">
                            <div class="item-check" onclick="toggleTask(${task.id})">${checkMark}</div>
                            <div class="item-text">${escapeHtml(task.title)}</div>
                            <span class="priority-badge priority-${task.priority}">${task.priority}</span>
                            <button class="item-delete" onclick="deleteItem('tasks', ${task.id})">✕</button>
                        </div>
                    `;
                });
                if (!data.data || data.data.length === 0) {
                    list.innerHTML = '<div style="text-align:center;padding:20px;color:var(--text-dim);">No tasks yet</div>';
                }
            });
    } else if (name === 'reminders') {
        fetch('/api/reminders')
            .then(r => r.json())
            .then(data => {
                const list = document.getElementById('remindersList');
                list.innerHTML = '';
                (data.data || []).forEach(rem => {
                    list.innerHTML += `
                        <div class="panel-list-item">
                            <div class="item-text">${escapeHtml(rem.text)}</div>
                            <div class="item-meta">⏰ ${rem.remind_at || ''}</div>
                            <button class="item-delete" onclick="deleteItem('reminders', ${rem.id})">✕</button>
                        </div>
                    `;
                });
                if (!data.data || data.data.length === 0) {
                    list.innerHTML = '<div style="text-align:center;padding:20px;color:var(--text-dim);">No reminders yet</div>';
                }
            });
    }
}

function deleteItem(type, id) {
    const endpoints = {notes: '/api/notes', tasks: '/api/tasks', reminders: '/api/reminders'};
    fetch(endpoints[type], {
        method: 'DELETE',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({id: id})
    }).then(() => loadPanelData(type));
}

function toggleTask(id) {
    fetch('/api/tasks', {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({id: id})
    }).then(() => loadPanelData('tasks'));
}

// ══════════════════════════════════════════════════════
// PARTICLE SYSTEM
// ══════════════════════════════════════════════════════
const canvas = document.getElementById('particleCanvas');
const ctx = canvas.getContext('2d');
let particles = [];

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

class Particle {
    constructor() {
        this.reset();
    }

    reset() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 1.5 + 0.3;
        this.speedX = (Math.random() - 0.5) * 0.3;
        this.speedY = (Math.random() - 0.5) * 0.3;
        this.opacity = Math.random() * 0.4 + 0.1;
    }

    update() {
        this.x += this.speedX;
        this.y += this.speedY;

        if (this.x < 0 || this.x > canvas.width || this.y < 0 || this.y > canvas.height) {
            this.reset();
        }
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(0, 212, 255, ${this.opacity})`;
        ctx.fill();
    }
}

// Create particles
for (let i = 0; i < 60; i++) {
    particles.push(new Particle());
}

function animateParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw connections
    for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
            const dx = particles[i].x - particles[j].x;
            const dy = particles[i].y - particles[j].y;
            const dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < 120) {
                ctx.beginPath();
                ctx.strokeStyle = `rgba(0, 212, 255, ${0.08 * (1 - dist / 120)})`;
                ctx.lineWidth = 0.5;
                ctx.moveTo(particles[i].x, particles[i].y);
                ctx.lineTo(particles[j].x, particles[j].y);
                ctx.stroke();
            }
        }
    }

    particles.forEach(p => {
        p.update();
        p.draw();
    });

    requestAnimationFrame(animateParticles);
}
animateParticles();

// ══════════════════════════════════════════════════════
// KEYBOARD SHORTCUTS
// ══════════════════════════════════════════════════════
document.addEventListener('keydown', (e) => {
    // Ctrl+K to focus input
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        commandInput.focus();
    }

    // Escape to close panels
    if (e.key === 'Escape') {
        closeAllPanels();
        stopListening();
    }
});

// Focus input on page load
setTimeout(() => commandInput.focus(), 500);

console.log('%c J.A.R.V.I.S. %c Online ', 
    'background: #0080ff; color: white; padding: 4px 8px; border-radius: 4px 0 0 4px; font-weight: bold;',
    'background: #00d4ff; color: black; padding: 4px 8px; border-radius: 0 4px 4px 0;'
);

// ══════════════════════════════════════════════════════
// WEATHER WIDGET
// ══════════════════════════════════════════════════════
function fetchWeather() {
    fetch('/api/weather?city=auto')
        .then(r => r.json())
        .then(data => {
            const el = document.getElementById('weatherWidget');
            if (el && data.success && data.data) {
                const w = data.data;
                el.innerHTML = `
                    <div class="weather-temp">${w.temp}°C</div>
                    <div class="weather-desc">${w.desc}</div>
                    <div class="weather-details">
                        <span>💧 ${w.humidity}%</span>
                        <span>🌬️ ${w.wind} km/h</span>
                    </div>
                `;
            }
        })
        .catch(() => {});
}
fetchWeather();
setInterval(fetchWeather, 300000); // Update every 5 min
