# J.A.R.V.I.S. — Project Explanation Guide
### For College Viva, Internal Review, and Submission Preparation

---

## 1. What is J.A.R.V.I.S.?

J.A.R.V.I.S. stands for **Just A Rather Very Intelligent System**. It is a full-stack, AI-powered personal assistant web application built using Python, Flask, and the Anthropic Claude AI API.

The project is inspired by Tony Stark's AI assistant from the Marvel Cinematic Universe. The goal is to build a **real, functional equivalent** — a web-based command centre that:

- Understands both **voice and text commands**
- Executes **system-level operations** (open apps, take screenshots, control volume)
- Manages **personal productivity** (notes, tasks, reminders)
- Fetches **live information** (weather, news, Wikipedia)
- Conducts **intelligent AI conversations** using Claude Sonnet
- Displays a real-time **Iron Man HUD dashboard** with live system statistics

---

## 2. How Does It Work? (Step-by-Step)

### Step 1 — User Sends a Command
The user types into the input box or clicks the microphone and speaks. If voice is used, the **Web Speech API** (browser-native) transcribes the speech to text. The text is then sent to the Flask server via **WebSocket** (not a regular HTTP request).

### Step 2 — Server Receives the Command
The Flask-SocketIO server receives the `command` event. It immediately emits a `status: processing` event back to the browser so the user sees a "Processing…" indicator.

### Step 3 — Intent Detection (Layer 1 — Fast)
The `process_command()` function in `app.py` evaluates the command against a large series of keyword patterns using Python string matching and regular expressions. This covers 50+ command categories. If a match is found here, the response is generated in **under 10 milliseconds** without any external API call.

```
"what time is it?"    → info_provider.get_time()
"open notepad"        → system_actions.open_application("notepad")
"latest tech news"    → news_fetcher.get_news_text("tech")
"add note: Buy milk"  → notes_manager.add_note_quick("Buy milk")
```

### Step 4 — CSV Intent Detector (Layer 1 Fallback)
If no keyword pattern matches, the `IntentDetector` class is used. It loads a CSV file of known commands (os_dataset.csv) and computes the **Jaccard similarity** between the user's input and each known command. Jaccard similarity = (words in common) ÷ (total unique words). If the best match score exceeds 0.35, the matched intent is dispatched.

### Step 5 — Claude AI (Layer 2 — Smart Fallback)
If the intent detector also fails to find a confident match, the command is sent to the **Claude Sonnet API** (via HTTP POST to api.anthropic.com). The AI module sends the full conversation history (last 10 exchanges) plus a detailed system prompt that instructs Claude to behave as J.A.R.V.I.S. — refined British tone, address user as "sir", concise but complete answers.

### Step 6 — Logging
After getting a response from any of the three layers, the interaction (command, response, intent, action_type, timestamp) is saved to the **SQLite database** in the `logs` table.

### Step 7 — Response Delivery
The server emits a `response` WebSocket event back to the browser with the response text, detected intent, action type, and an optional URL to open (for web actions). The browser renders the response in the chat panel and uses the **SpeechSynthesis API** to read it aloud.

### Step 8 — Background Threads
Two Python daemon threads run continuously in the background:
- **`system_stats_loop`:** Every 2 seconds, reads CPU%, RAM%, Disk%, Network I/O, and Battery using `psutil` and emits a `system_stats` WebSocket event. The HUD updates in real time.
- **`reminder_check_loop`:** Monitors the reminders table and emits a WebSocket alert when a reminder's `remind_at` time is reached.

---

## 3. Project Architecture Explained

### Three-Tier Architecture

| Tier | What It Is | Technologies |
|---|---|---|
| **Tier 1: Presentation** | The browser interface the user sees and interacts with | HTML5, CSS3, JavaScript, Web Speech API, SpeechSynthesis, Socket.IO client |
| **Tier 2: Application** | The Python server that processes commands and runs business logic | Flask, Flask-SocketIO, 18 Python modules, Claude API |
| **Tier 3: Data** | The database that stores all user data | SQLite3, jarvis.db |

### Communication Flow

```
Browser ←──WebSocket (Socket.IO)──→ Flask Server ←──sqlite3──→ SQLite DB
Browser ←──HTTP REST API──────────→ Flask Server
Flask Server ←──HTTPS──────────────→ Claude API (Anthropic)
Flask Server ←──HTTPS──────────────→ OpenWeather API
Flask Server ←──HTTPS──────────────→ NewsAPI
Flask Server ←──HTTPS──────────────→ Wikipedia API
```

---

## 4. Key Technical Concepts Explained

### What is WebSocket?
HTTP is a one-directional protocol — the browser sends a request and the server responds, then the connection closes. WebSocket is different: it keeps a **persistent, bidirectional connection** open between the browser and the server. This means the server can push data to the browser at any time without the browser asking for it. This is how the system stats update every 2 seconds and how reminder alerts appear automatically.

### What is Flask-SocketIO?
Flask-SocketIO is a Flask extension that adds WebSocket support. It uses the **Socket.IO protocol**, which is built on top of WebSocket but adds fallback mechanisms for older browsers and automatic reconnection. In the code, server events are decorated with `@socketio.on('event_name')` and the server emits events with `emit('event_name', data)`.

### What is Jaccard Similarity?
Jaccard similarity measures how similar two sets of words are.

```
User input tokens:  {"open", "the", "chrome", "browser"}
Known pattern:      {"open", "chrome"}

Intersection = {"open", "chrome"} → size = 2
Union = {"open", "the", "chrome", "browser"} → size = 4

Jaccard = 2 / 4 = 0.5  (50% similar → above threshold 0.35 → MATCH)
```

### What is Claude Sonnet?
Claude Sonnet is a large language model (LLM) developed by Anthropic. It is accessed via a REST API — the Flask server sends an HTTP POST request to `api.anthropic.com/v1/messages` with the conversation history and a system prompt. The model returns a text response which J.A.R.V.I.S. delivers to the user. The system prompt instructs the model to behave with a British tone and address the user as "sir".

### What is TextBlob Sentiment Analysis?
TextBlob is a Python NLP library. Its sentiment analyser evaluates text and returns a **polarity score** from -1.0 (very negative) to +1.0 (very positive) and a **subjectivity score** from 0.0 (objective) to 1.0 (subjective). J.A.R.V.I.S. uses this to analyse the emotional tone of any text the user submits.

### What is SQLite?
SQLite is a lightweight, file-based, serverless relational database. Unlike PostgreSQL or MySQL, it runs entirely within the Python process — no separate database server is needed. The entire database is stored in a single file: `data/jarvis.db`. Python includes the `sqlite3` module in its standard library, so no extra installation is required.

---

## 5. Database Design

J.A.R.V.I.S. uses a flat schema with **5 independent tables**, all managed by the `DatabaseManager` class in `core/database.py`.

```sql
-- Stores every command and response pair
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    command TEXT NOT NULL,
    response TEXT NOT NULL,
    intent TEXT,
    action_type TEXT,
    timestamp TEXT NOT NULL
);

-- User notes (pinnable, categorised)
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category TEXT DEFAULT 'general',
    pinned INTEGER DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- User to-do tasks with priority and completion
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    priority TEXT DEFAULT 'medium',
    done INTEGER DEFAULT 0,
    created_at TEXT NOT NULL,
    completed_at TEXT
);

-- Timed reminders with background monitoring
CREATE TABLE reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    remind_at TEXT,
    done INTEGER DEFAULT 0,
    created_at TEXT NOT NULL
);

-- Key-value store for user preferences
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
```

---

## 6. Module Descriptions

| Module | File | What It Does |
|---|---|---|
| AI Chat | `modules/ai_chat.py` | Sends messages to Claude Sonnet API with rolling conversation memory |
| Calculator | `modules/calculator.py` | Evaluates math expressions and converts units (km, kg, celsius, etc.) |
| Entertainment | `modules/entertainment.py` | Returns jokes, motivational quotes, fun facts, and trivia questions |
| File Manager | `modules/file_manager.py` | Lists directory contents, searches for files, reports disk usage |
| Information | `modules/information.py` | Returns current time, date, weather (OpenWeather), help text |
| Knowledge | `modules/knowledge.py` | Searches Wikipedia and returns a clean summary |
| News | `modules/news.py` | Fetches headlines from NewsAPI by category |
| Notes | `modules/notes.py` | Adds, lists, and searches notes via DatabaseManager |
| Planner | `modules/planner.py` | Adds and lists tasks with priority management |
| Reminders | `modules/reminders.py` | Adds reminders and runs the background time-check loop |
| Security Tools | `modules/security_tools.py` | Generates passwords, computes SHA-256 hashes, base64 encode/decode |
| Sentiment | `modules/sentiment.py` | Analyses text sentiment using TextBlob + custom word lists |
| Summarizer | `modules/summarizer.py` | Summarises long text into key points |
| System Actions | `modules/system_actions.py` | Opens/closes apps, screenshots, locks screen, controls volume, reads system info |
| Translator | `modules/translator.py` | Translates text to supported languages |
| Voice Engine | `modules/voice_engine.py` | Manages server-side pyttsx3 TTS and SpeechRecognition microphone input |
| Web Actions | `modules/web_actions.py` | Opens websites, runs Google and YouTube searches |
| Intent Detector | `core/intent_detector.py` | CSV-based Jaccard similarity classifier for fast command routing |

---

## 7. Command Flow Summary

```
User Input
    │
    ▼
process_command()  ─────────────────────────────────────────────────────────┐
    │                                                                        │
    ├── Time/Date queries       → info_provider.get_time() / get_date()     │
    ├── Weather queries         → info_provider.get_weather(city)           │
    ├── System commands         → system_actions.*                          │
    ├── Web actions             → web_actions.*                             │
    ├── Notes commands          → notes_manager.*                           │
    ├── Task commands           → task_planner.*                            │
    ├── Reminder commands       → reminder_manager.*                        │
    ├── Calculator/Convert      → smart_calculator.*                        │
    ├── Translation             → translator.*                              │
    ├── News commands           → news_fetcher.*                            │
    ├── Knowledge queries       → knowledge_base.*                          │
    ├── Entertainment           → entertainment.*                           │
    ├── Security tools          → security_tools.*                          │
    ├── Sentiment/Summarize     → sentiment_analyzer.* / text_summarizer.*  │
    ├── File manager            → file_manager.*                            │
    ├── Greeting/Social         → built-in responses                        │
    │                                                                        │
    ├── [NO MATCH] ────────────→ intent_detector.detect_intent()           │
    │       ├── [confidence ≥ 0.35] → _dispatch_intent()                   │
    │       └── [confidence < 0.35] → ai_chat.get_response()  ─────────────┘
    │
    └── db.log_interaction() → SQLite logs table
              │
              └── emit('response', {...}) → Browser → SpeechSynthesis TTS
```

---

## 8. Why These Technologies Were Chosen

| Technology | Reason for Choice |
|---|---|
| **Flask** | Lightweight, minimal framework ideal for small-to-medium Python web apps. Easy to learn, flexible, large community. |
| **Flask-SocketIO** | Only WebSocket library with native Flask integration. Supports background threads and room-based broadcasting. |
| **Claude Sonnet** | State-of-the-art LLM from Anthropic with strong reasoning, follows complex personas via system prompts, reliable API. |
| **SQLite** | Zero setup — no database server needed. Ideal for a locally-running single-user personal assistant. Built into Python. |
| **Web Speech API** | Browser-native, no installation needed, works in Chrome with no additional server cost. |
| **TextBlob** | Simple, reliable NLP library for offline sentiment analysis without needing an external API. |
| **psutil** | Cross-platform system monitoring library. Works on Windows, macOS, and Linux. |

---

## 9. Challenges and Solutions

| Challenge | Solution |
|---|---|
| Real-time stats without constant API calls | Background daemon thread with `socketio.emit()` every 2 seconds |
| Conversation memory across multiple turns | Rolling list of `{"role": ..., "content": ...}` dicts passed on every Claude API call |
| Handling both voice and typed commands uniformly | Both inputs send the same `command` WebSocket event — server treats them identically |
| Avoiding Claude API call for every simple command | Two-layer approach: keyword router + Jaccard CSV classifier before hitting the AI |
| Reminders firing at the right time | Separate daemon thread continuously checks `remind_at` timestamps every 30 seconds |
| System stats blocking the main thread | `async_mode='threading'` on SocketIO + daemon thread prevents any event loop blocking |

---

## 10. How to Demo for Viva

### Recommended Demo Sequence

1. **Open** `http://localhost:5000` — show the HUD loading with animated arc reactor
2. **Type:** `good morning` — show the daily briefing (date, time, tasks, reminders, news headline)
3. **Type:** `what time is it?` — instant response (shows local intent routing, no API call)
4. **Type:** `open notepad` — notepad opens on the system (shows OS integration)
5. **Type:** `system info` — show CPU, RAM, disk, OS details
6. **Click mic:** Speak `tell me a joke` — show voice input → response → TTS readback
7. **Type:** `add note: Remember to bring project documents` — show note saved
8. **Type:** `show my notes` — show the saved note
9. **Type:** `add task: Submit BCA project high` — show task created
10. **Type:** `show my tasks` — show pending task with HIGH priority label
11. **Type:** `generate password 16` — show secure password generated
12. **Type:** `what is machine learning?` — show Claude AI responding (complex query)
13. **Type:** `latest tech news` — show 6 headlines from NewsAPI
14. **Point to HUD panels** — show live CPU/RAM/Disk updating every 2 seconds
15. **Open** `http://localhost:5000/api/logs` — show JSON API response (proves REST works)

### Key Points to Explain During Viva

- The system has **two AI layers** — explain Jaccard similarity vs Claude API
- The WebSocket keeps a **persistent connection** — not HTTP polling
- All user data is **stored locally** in SQLite — no cloud dependency for productivity features
- The system works **offline** for most features — only AI chat, weather, and news need internet
- The **modular design** means each module is independent and can be extended

---

## 11. Viva Q&A Preparation

See `VIVA_QA.md` for the complete viva question and answer guide.
