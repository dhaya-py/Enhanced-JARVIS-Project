/* ═══════════════════════════════════════════════════════════════
   J.A.R.V.I.S. — Frontend Engine v3.0
   Socket.io · Web Speech API · All panel logic
   ═══════════════════════════════════════════════════════════════ */

'use strict';

// ── State ──────────────────────────────────────────────────────────────────
const state = {
  socket: null,
  voiceActive: false,
  isSpeaking: false,
  isProcessing: false,
  recognition: null,
  synth: window.speechSynthesis,
  voices: [],
  msgCount: 0,
  startTime: Date.now(),
  vizInterval: null,
  currentTab: 'history',
  cmdCount: 0,
};

// ── DOM refs ───────────────────────────────────────────────────────────────
const $ = id => document.getElementById(id);
const convo     = $('convo');
const cmdInput  = $('cmd-input');
const micBtn    = $('mic-btn');
const arcState  = $('arc-state');
const arcSub    = $('arc-sub');
const vizEl     = $('viz');

// ── Boot Sequence ──────────────────────────────────────────────────────────
const BOOT_LINES = [
  '> INITIALIZING JARVIS CORE SYSTEMS...',
  '> LOADING NEURAL INTENT ENGINE (85 PATTERNS)... OK',
  '> CONNECTING FLASK + SOCKETIO BACKEND.......... OK',
  '> MOUNTING COGNITIVE MODULES................... OK',
  '> AI ENGINE: CLAUDE SONNET LINKED.............. OK',
  '> VOICE SYNTHESIS ENGINE....................... OK',
  '> SPEECH RECOGNITION MODULE.................... OK',
  '> DATABASE (SQLITE) CONNECTED.................. OK',
  '> NOTES / TASKS / REMINDERS SYSTEMS............ OK',
  '> KNOWLEDGE BASE & NEWS FETCHER................ OK',
  '> SECURITY TOOLS & CALCULATOR LOADED........... OK',
  '> SYSTEM DIAGNOSTICS MONITOR ACTIVE............ OK',
  '> ALL SYSTEMS NOMINAL — J.A.R.V.I.S. ONLINE...',
];

async function runBoot() {
  const logEl   = $('boot-log');
  const progEl  = $('boot-progress');
  for (let i = 0; i < BOOT_LINES.length; i++) {
    await delay(220);
    const line = document.createElement('div');
    line.className = 'line';
    line.textContent = BOOT_LINES[i];
    if (BOOT_LINES[i].includes('OK')) line.style.color = '#00d4ff';
    logEl.appendChild(line);
    progEl.style.width = ((i + 1) / BOOT_LINES.length * 100) + '%';
  }
  await delay(500);
  const bs = $('boot-screen');
  bs.style.transition = 'opacity .8s ease';
  bs.style.opacity = '0';
  await delay(800);
  bs.style.display = 'none';

  const app = $('app');
  app.style.display = 'grid';
  await delay(40);
  app.classList.add('visible');

  initSocket();
  initClock();
  loadAllTabs();
  loadNewsTicker();
  await delay(800);
  addMsg('Good day, sir. J.A.R.V.I.S. v3.0 is fully operational. All systems are running nominally. How may I assist you?', 'jarvis');
  speak('Good day, sir. J.A.R.V.I.S. is fully operational. How may I assist you?');
}

// ── Socket.io ──────────────────────────────────────────────────────────────
function initSocket() {
  state.socket = io({ transports: ['websocket', 'polling'] });
  const s = state.socket;

  s.on('connect', () => {
    setConnStatus(true);
    $('ft-socket').textContent = 'CONNECTED';
    $('ft-socket').style.color = '#00ff88';
  });
  s.on('disconnect', () => {
    setConnStatus(false);
    $('ft-socket').textContent = 'OFFLINE';
    $('ft-socket').style.color = '#e63946';
  });
  s.on('connected', d => toast('J.A.R.V.I.S. online — ' + d.ts));

  s.on('status', d => {
    arcSub.textContent = d.msg.toUpperCase();
    if (d.state === 'processing') setArcState('PROCESSING...', true);
    else if (d.state === 'ready') setArcState('SYSTEMS ONLINE', false);
  });

  s.on('response', d => {
    hideTyping();
    addMsg(d.text, 'jarvis', d.intent, d.action_type);
    if (d.open_url) openUrl(d.open_url);
    speak(d.text);
    refreshHistoryIfActive();
    state.isProcessing = false;
    setArcState('SYSTEMS ONLINE', false);
    stopViz();
  });

  s.on('voice_recognized', d => {
    addMsg(d.text, 'user');
    showTyping();
    startViz();
  });

  s.on('system_stats', d => updateStats(d));

  s.on('news_ticker', d => {
    if (d.items && d.items.length) updateTicker(d.items);
  });

  s.on('reminder_alert', d => showReminderAlert(d));
}

function setConnStatus(online) {
  const dot   = $('conn-dot');
  const label = $('conn-label');
  dot.className   = 'conn-dot ' + (online ? 'online' : 'offline');
  label.textContent = online ? 'ONLINE' : 'OFFLINE';
}

// ── Send Command ───────────────────────────────────────────────────────────
function sendCmd(text) {
  if (state.isProcessing) return;
  const input = text || cmdInput.value.trim();
  if (!input) return;
  cmdInput.value = '';

  addMsg(input, 'user');
  state.isProcessing = true;
  setArcState('PROCESSING...', true);
  showTyping();
  startViz();

  if (state.socket && state.socket.connected) {
    state.socket.emit('command', { text: input });
  } else {
    // Fallback: direct fetch
    hideTyping();
    addMsg('Socket not connected. Please refresh the page, sir.', 'jarvis');
    state.isProcessing = false;
    setArcState('SYSTEMS ONLINE', false);
    stopViz();
  }
}

// ── Messages ───────────────────────────────────────────────────────────────
function addMsg(text, role, intent, actionType) {
  const wrap = document.createElement('div');
  wrap.className = `msg ${role}`;

  const ts = new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
  const intentHtml = (intent && role === 'jarvis')
    ? `<span class="intent-tag">${intent}</span>`
    : '';

  wrap.innerHTML = `
    <div class="avatar">${role === 'user' ? 'YOU' : 'JRV'}</div>
    <div>
      <div class="bubble">${esc(text).replace(/\n/g, '<br>')}</div>
      <div class="msg-meta">${ts}${intentHtml}</div>
    </div>`;

  convo.appendChild(wrap);
  convo.scrollTop = convo.scrollHeight;
  state.msgCount++;
  state.cmdCount++;
  $('msg-count-lbl').textContent = `${state.msgCount} EXCHANGE${state.msgCount !== 1 ? 'S' : ''}`;
  $('hdr-cmdcount').textContent = state.cmdCount;
}

function showTyping() {
  const d = document.createElement('div');
  d.className = 'msg jarvis'; d.id = 'typing-ind';
  d.innerHTML = `<div class="avatar">JRV</div>
    <div><div class="bubble"><div class="typing-dots"><span></span><span></span><span></span></div></div></div>`;
  convo.appendChild(d);
  convo.scrollTop = convo.scrollHeight;
}
function hideTyping() { $('typing-ind')?.remove(); }

function clearConvo() {
  convo.innerHTML = '';
  state.msgCount = 0;
  $('msg-count-lbl').textContent = '0 EXCHANGES';
  addMsg('Conversation cleared, sir. How may I assist you?', 'jarvis');
}

// ── Arc / Status ───────────────────────────────────────────────────────────
function setArcState(text, processing = false) {
  arcState.textContent = text;
  const arc = $('arcReactor');
  arc.style.filter = processing
    ? 'drop-shadow(0 0 20px rgba(230,57,70,.8))'
    : '';
}

// ── Voice Visualizer ───────────────────────────────────────────────────────
const vizBars = () => document.querySelectorAll('.vb');
function startViz() {
  clearInterval(state.vizInterval);
  state.vizInterval = setInterval(() => {
    vizBars().forEach(b => { b.style.height = (Math.random() * 22 + 3) + 'px'; });
  }, 100);
}
function stopViz() {
  clearInterval(state.vizInterval);
  vizBars().forEach(b => { b.style.height = '3px'; });
}

// ── Speech Synthesis ───────────────────────────────────────────────────────
function loadVoices() {
  state.voices = state.synth.getVoices();
}
if (state.synth) {
  loadVoices();
  state.synth.onvoiceschanged = loadVoices;
}

function speak(text) {
  if (!state.synth || !text) return;
  state.synth.cancel();
  const clean = text.replace(/\n/g, ' ').replace(/[*_`]/g, '').substring(0, 400);
  const utter = new SpeechSynthesisUtterance(clean);
  utter.lang   = 'en-GB';
  utter.rate   = 1.0;
  utter.pitch  = 0.9;
  utter.volume = 0.9;

  const pref = state.voices.find(v => /female|zira|samantha|victoria/i.test(v.name) && v.lang.startsWith('en'))
    || state.voices.find(v => v.lang.startsWith('en-GB'))
    || state.voices.find(v => v.lang.startsWith('en'));
  if (pref) utter.voice = pref;

  utter.onstart = () => {
    state.isSpeaking = true;
    arcSub.textContent = 'SPEAKING...';
    $('ft-voice').textContent = 'ACTIVE';
    $('ft-voice').style.color = '#00d4ff';
    startViz();
  };
  utter.onend = () => {
    state.isSpeaking = false;
    arcSub.textContent = 'READY FOR COMMANDS';
    $('ft-voice').textContent = 'STANDBY';
    $('ft-voice').style.color = '';
    stopViz();
    if (state.voiceActive && !state.isProcessing) startListening();
  };
  state.synth.speak(utter);
}

// ── Speech Recognition ─────────────────────────────────────────────────────
function toggleVoice() {
  state.voiceActive ? stopListening() : startListening();
}

function startListening() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) { toast('Speech recognition not supported. Use Chrome, sir.'); return; }

  state.recognition = new SR();
  state.recognition.lang            = 'en-US';
  state.recognition.continuous      = false;
  state.recognition.interimResults  = true;

  state.recognition.onstart = () => {
    state.voiceActive = true;
    micBtn.classList.add('listening');
    $('arc-state').textContent = 'LISTENING...';
    arcSub.textContent          = 'SPEAK YOUR COMMAND';
    $('ft-voice').textContent  = 'LISTENING';
    $('ft-voice').style.color  = '#e63946';
    startViz();
  };

  state.recognition.onresult = e => {
    let final = '';
    for (let i = e.resultIndex; i < e.results.length; i++) {
      if (e.results[i].isFinal) final += e.results[i][0].transcript;
      else cmdInput.value = e.results[i][0].transcript;
    }
    if (final) { cmdInput.value = final; sendCmd(final); }
  };

  state.recognition.onerror = e => {
    if (e.error !== 'aborted') toast(`Voice error: ${e.error}`);
    stopListening();
  };

  state.recognition.onend = () => {
    if (state.voiceActive && !state.isSpeaking && !state.isProcessing) {
      setTimeout(startListening, 300);
    } else {
      stopListening();
    }
  };

  state.recognition.start();
}

function stopListening() {
  state.voiceActive = false;
  state.recognition?.stop();
  micBtn.classList.remove('listening');
  arcState.textContent = 'SYSTEMS ONLINE';
  arcSub.textContent   = 'READY FOR COMMANDS';
  $('ft-voice').textContent = 'STANDBY';
  $('ft-voice').style.color = '';
  stopViz();
}

// ── System Stats ───────────────────────────────────────────────────────────
function updateStats(d) {
  setBar('cpu', d.cpu, d.cpu.toFixed(1) + '%');
  setBar('ram', d.ram, d.ram.toFixed(1) + '%');
  setBar('disk', d.disk, d.disk + '%');
  if (d.battery !== null && d.battery !== undefined) {
    setBar('bat', d.battery, d.battery + '%' + (d.plugged ? ' ⚡' : ''));
  } else {
    $('bat-val').textContent = 'N/A';
  }
  $('net-sent').textContent = d.net_sent + ' MB';
  $('net-recv').textContent = d.net_recv + ' MB';
}
function setBar(name, pct, label) {
  const bar = $(`${name}-bar`);
  const val = $(`${name}-val`);
  if (bar) bar.style.width = Math.min(pct, 100) + '%';
  if (val) val.textContent = label;
}

// ── Clock / Uptime ─────────────────────────────────────────────────────────
function initClock() {
  setInterval(() => {
    const now = new Date();
    $('live-clock').textContent = now.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    $('live-date').textContent  = now.toLocaleDateString('en-IN', { weekday: 'long', year: 'numeric', month: 'short', day: 'numeric' }).toUpperCase();
    const up = Math.floor((Date.now() - state.startTime) / 1000);
    $('uptime').textContent = [
      String(Math.floor(up / 3600)).padStart(2, '0'),
      String(Math.floor((up % 3600) / 60)).padStart(2, '0'),
      String(up % 60).padStart(2, '0'),
    ].join(':');
  }, 1000);
}

// ── News Ticker ────────────────────────────────────────────────────────────
function loadNewsTicker() {
  if (state.socket) state.socket.emit('get_news_ticker');
}
function updateTicker(items) {
  const track = $('ticker-track');
  const text = items.map(i => `${i.title} [${i.source || 'NEWS'}]`).join('  ◆  ');
  track.innerHTML = `<span>${text}</span>`;
}

// ── URL opener ────────────────────────────────────────────────────────────
function openUrl(url) {
  if (url) window.open(url, '_blank', 'noopener');
}

// ── Tabs ───────────────────────────────────────────────────────────────────
function switchTab(tab) {
  state.currentTab = tab;
  document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.tab === tab));
  document.querySelectorAll('.tab-content').forEach(c => c.classList.toggle('active', c.id === `tab-${tab}`));
  if (tab === 'history') loadHistory();
  else if (tab === 'notes') loadNotes();
  else if (tab === 'tasks') loadTasks();
  else if (tab === 'reminders') loadReminders();
}

function loadAllTabs() { loadHistory(); loadNotes(); loadTasks(); loadReminders(); }
function refreshHistoryIfActive() { if (state.currentTab === 'history') loadHistory(); }

// ── History ────────────────────────────────────────────────────────────────
async function loadHistory() {
  const list = $('history-list');
  try {
    const r = await fetch('/api/logs?limit=40');
    const d = await r.json();
    if (!d.data || !d.data.length) { list.innerHTML = '<div class="empty-state">No history yet, sir.</div>'; return; }
    list.innerHTML = d.data.map(h => `
      <div class="hist-item">
        <div class="hist-cmd">${esc(h.command)}</div>
        <div class="hist-resp">${esc(h.response)}</div>
        <div class="hist-ts">${h.timestamp || ''}</div>
      </div>`).join('');
    $('hdr-cmdcount').textContent = d.data.length;
  } catch(e) { list.innerHTML = '<div class="empty-state">Failed to load history.</div>'; }
}

async function clearHistory() {
  await fetch('/api/logs/clear', { method: 'POST' });
  loadHistory();
  toast('History cleared, sir.');
}

// ── Notes ──────────────────────────────────────────────────────────────────
async function loadNotes() {
  const list = $('notes-list');
  try {
    const r = await fetch('/api/notes');
    const d = await r.json();
    $('hdr-notecount').textContent = d.data ? d.data.length : 0;
    if (!d.data || !d.data.length) { list.innerHTML = '<div class="empty-state">No notes yet, sir.</div>'; return; }
    list.innerHTML = d.data.map(n => `
      <div class="note-item">
        <div class="note-title">${esc(n.title)}</div>
        <div class="note-body">${esc(n.content)}</div>
        <div class="note-cat">${n.category.toUpperCase()} · ${n.created_at}</div>
        <button class="item-del" onclick="deleteNote(${n.id})">✕</button>
      </div>`).join('');
  } catch(e) { list.innerHTML = '<div class="empty-state">Failed to load notes.</div>'; }
}

function showAddNote() { $('note-form').classList.remove('hidden'); }
function hideAddNote() { $('note-form').classList.add('hidden'); $('note-title').value = ''; $('note-content').value = ''; }

async function addNote() {
  const title   = $('note-title').value.trim();
  const content = $('note-content').value.trim();
  if (!title || !content) { toast('Title and content required, sir.'); return; }
  await fetch('/api/notes', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, content })
  });
  hideAddNote(); loadNotes();
  toast('Note saved, sir.');
}

async function deleteNote(id) {
  await fetch(`/api/notes/${id}`, { method: 'DELETE' });
  loadNotes();
  toast('Note deleted, sir.');
}

// ── Tasks ──────────────────────────────────────────────────────────────────
async function loadTasks() {
  const list = $('tasks-list');
  try {
    const r = await fetch('/api/tasks');
    const d = await r.json();
    if (!d.data || !d.data.length) { list.innerHTML = '<div class="empty-state">Task list clear, sir.</div>'; return; }
    list.innerHTML = d.data.map(t => `
      <div class="task-item">
        <input type="checkbox" class="task-check" ${t.done ? 'checked' : ''} onchange="toggleTask(${t.id})">
        <div class="task-title ${t.done ? 'done' : ''}">${esc(t.title)}</div>
        <span class="task-pri ${t.priority}">${t.priority.toUpperCase()}</span>
        <button class="item-del" onclick="deleteTask(${t.id})">✕</button>
      </div>`).join('');
  } catch(e) { list.innerHTML = '<div class="empty-state">Failed to load tasks.</div>'; }
}

function showAddTask() { $('task-form').classList.remove('hidden'); }
function hideAddTask() { $('task-form').classList.add('hidden'); $('task-title').value = ''; }

async function addTask() {
  const title    = $('task-title').value.trim();
  const priority = $('task-priority').value;
  if (!title) { toast('Please enter a task title, sir.'); return; }
  await fetch('/api/tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, priority })
  });
  hideAddTask(); loadTasks();
  toast('Task added, sir.');
}

async function toggleTask(id) {
  await fetch(`/api/tasks/${id}`, { method: 'PUT' });
  loadTasks();
}

async function deleteTask(id) {
  await fetch(`/api/tasks/${id}`, { method: 'DELETE' });
  loadTasks();
  toast('Task removed, sir.');
}

// ── Reminders ──────────────────────────────────────────────────────────────
async function loadReminders() {
  const list = $('reminders-list');
  try {
    const r = await fetch('/api/reminders');
    const d = await r.json();
    const active = d.data ? d.data.filter(r => !r.done) : [];
    if (!active.length) { list.innerHTML = '<div class="empty-state">No active reminders, sir.</div>'; return; }
    list.innerHTML = active.map(rem => `
      <div class="rem-item">
        <div class="rem-icon">🔔</div>
        <div class="rem-body">
          <div class="rem-text">${esc(rem.text)}</div>
          ${rem.remind_at ? `<div class="rem-time">At ${rem.remind_at}</div>` : ''}
        </div>
        <button class="item-del" onclick="deleteReminder(${rem.id})">✕</button>
      </div>`).join('');
  } catch(e) { list.innerHTML = '<div class="empty-state">Failed to load reminders.</div>'; }
}

function showAddReminder() { $('reminder-form').classList.remove('hidden'); }
function hideAddReminder() { $('reminder-form').classList.add('hidden'); $('rem-text').value = ''; $('rem-time').value = ''; }

async function addReminder() {
  const text     = $('rem-text').value.trim();
  const remind_at = $('rem-time').value || null;
  if (!text) { toast('Please enter reminder text, sir.'); return; }
  await fetch('/api/reminders', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, remind_at })
  });
  hideAddReminder(); loadReminders();
  toast('Reminder set, sir.');
}

async function deleteReminder(id) {
  await fetch(`/api/reminders/${id}`, { method: 'DELETE' });
  loadReminders();
  toast('Reminder cleared, sir.');
}

function showReminderAlert(d) {
  $('ra-text').textContent = d.text;
  $('reminder-alert').classList.remove('hidden');
  speak(`Reminder, sir: ${d.text}`);
  setTimeout(() => dismissReminder(), 10000);
}
function dismissReminder() { $('reminder-alert').classList.add('hidden'); }

// ── Toast ──────────────────────────────────────────────────────────────────
function toast(msg) {
  const t = $('toast');
  t.textContent = msg; t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}

// ── Helpers ────────────────────────────────────────────────────────────────
function esc(s) {
  if (!s) return '';
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}
function delay(ms) { return new Promise(r => setTimeout(r, ms)); }

// ── Init ───────────────────────────────────────────────────────────────────
window.addEventListener('load', () => {
  if (state.synth) { state.synth.getVoices(); }
  runBoot();
});

// Prevent accidental tab close during voice
window.addEventListener('beforeunload', () => { state.recognition?.stop(); state.synth?.cancel(); });
