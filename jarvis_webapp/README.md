# J.A.R.V.I.S. — AI Personal Assistant Web Application
### Just A Rather Very Intelligent System · Version 3.0

> *"At your service, sir."*

A full-stack AI-powered personal assistant web application built with **Python · Flask · Socket.IO · Claude AI**,  
featuring a real-time **Iron Man HUD interface**, voice interaction, system control, productivity management,  
and intelligent conversation backed by Anthropic's Claude Sonnet model.

---

## Student Information

| Field | Details |
|---|---|
| **Student Name** | Nasreen Fathima S |
| **Register No** | 212300358 |
| **Course** | Bachelor of Computer Applications (BCA) |
| **College** | Prof. Dhanapalan College of Science and Management, Kelambakkam |
| **Guide** | Dr. GM. Sridhar |
| **Year** | 2024–2025 |

---

## Quick Start

### Step 1 — Clone / Extract the Project
```bash
cd jarviswebapp
```

### Step 2 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Configure API Keys
```bash
cp .env.template .env
# Open .env and fill in your keys:
# ANTHROPIC_API_KEY=sk-ant-...      ← Required for full AI
# OPENWEATHER_API_KEY=...           ← Optional (weather)
# NEWS_API_KEY=...                  ← Optional (live news)
```

### Step 4 — Run the Application
```bash
python app.py
```

### Step 5 — Open in Browser
```
http://localhost:5000
```

> **Recommended browser:** Google Chrome (required for Web Speech API voice input)

---

## Project Structure

```
jarviswebapp/
│
├── app.py                    # Main Flask application & command dispatcher
├── requirements.txt          # All Python dependencies
├── .env                      # API keys (not committed to Git)
├── .env.template             # Template for environment setup
│
├── config/
│   ├── __init__.py
│   └── settings.py           # All configuration: API keys, model, ports, thresholds
│
├── core/
│   ├── __init__.py
│   ├── database.py           # SQLite DatabaseManager (5 tables: logs/notes/tasks/reminders/settings)
│   ├── intent_detector.py    # CSV-based Jaccard similarity intent classifier
│   ├── email.py              # Email notification (optional)
│   └── notifier.py           # System notification helper
│
├── modules/                  # 18 capability modules (one per domain)
│   ├── ai_chat.py            # Claude Sonnet integration with conversation memory
│   ├── calculator.py         # Smart calculator + unit converter
│   ├── entertainment.py      # Jokes, quotes, fun facts, trivia
│   ├── file_manager.py       # Disk usage, directory listing, file search
│   ├── information.py        # Time, date, weather, about, help
│   ├── knowledge.py          # Wikipedia-based knowledge search
│   ├── news.py               # NewsAPI headlines fetcher
│   ├── notes.py              # Notes manager (add/show/search)
│   ├── planner.py            # Task planner (add/show/toggle)
│   ├── reminders.py          # Reminder manager + background alert loop
│   ├── security_tools.py     # Password generator, hash, base64, strength check
│   ├── sentiment.py          # TextBlob sentiment analysis
│   ├── summarizer.py         # Text summarisation
│   ├── system_actions.py     # OS control: open/close apps, screenshot, volume, lock
│   ├── translator.py         # Language translation
│   ├── voice_engine.py       # pyttsx3 TTS + SpeechRecognition server-side
│   └── web_actions.py        # Open websites, Google/YouTube search
│
├── data/
│   ├── jarvis.db             # SQLite database (auto-created on first run)
│   └── os_dataset.csv        # Intent training dataset (command, intent, action_type)
│
├── templates/
│   └── index.html            # Single-page HUD frontend
│
└── static/
    ├── css/
    │   └── jarvis.css        # Iron Man HUD theme styles
    └── js/
        └── jarvis.js         # Socket.IO client, Web Speech API, TTS, panel logic
```

---

## Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Backend** | Python 3.10 | Primary programming language |
| **Web Framework** | Flask 3.0 | HTTP routing and template serving |
| **Real-time** | Flask-SocketIO 5.3.6 | WebSocket bidirectional communication |
| **AI Engine** | Claude Sonnet (Anthropic API) | Conversational AI with memory |
| **Intent Detection** | Custom CSV + Jaccard Similarity | Fast local command routing |
| **NLP** | TextBlob 0.18.0 | Sentiment analysis |
| **System Monitor** | psutil 5.9.8 | CPU, RAM, disk, battery metrics |
| **Database** | SQLite3 (stdlib) | Local persistent storage |
| **TTS (server)** | pyttsx3 2.90 | Server-side text-to-speech |
| **Speech Input** | SpeechRecognition 3.10.4 | Server-side speech-to-text |
| **Automation** | pyautogui 0.9.54 | Screenshot and keyboard control |
| **Frontend** | HTML5 + CSS3 + JavaScript | HUD interface |
| **Speech (browser)** | Web Speech API | Browser voice input |
| **TTS (browser)** | SpeechSynthesis API | British-accent voice output |
| **Knowledge** | wikipedia-api 0.6.0 | Wikipedia search |
| **News** | NewsAPI (requests) | Live news headlines |
| **Weather** | OpenWeather API (requests) | Real-time weather data |

---

## Features

### Voice & Text Interaction
- Click the **Arc Reactor** or microphone button to activate voice input
- Web Speech API transcribes speech → sends to server via WebSocket
- SpeechSynthesis API reads responses aloud (British accent)
- Automatically resumes listening after speaking

### AI Intelligence (Hybrid Two-Layer)
- **Layer 1 — Local Intent Detector:** Keyword routing + Jaccard similarity against `os_dataset.csv` for instant response to common commands (< 10ms)
- **Layer 2 — Claude Sonnet AI:** Complex or unrecognised queries route to Claude API with full session conversation memory

### System Commands
```
open notepad / chrome / calculator / vscode
close chrome / notepad
take screenshot
lock screen
volume 60 / volume up / volume down
system info / system status
list processes
shutdown / restart / sleep
```

### Web Actions
```
search for Python tutorials
google machine learning
open youtube / github / gmail
youtube search lo-fi music
```

### Productivity
```
add note: Buy groceries tomorrow
show my notes
add task: Complete project (high priority)
show my tasks
remind me to drink water
show my reminders
```

### Information & Knowledge
```
what time is it?
what date is today?
weather in Chennai
who is Alan Turing?
what is quantum computing?
tell me about the solar system
```

### Calculator & Conversion
```
calculate 450 / 9 + 12
convert 100 km to miles
convert 5 kg to pounds
```

### News & Entertainment
```
latest tech news
science headlines
tell me a joke
give me a quote
fun fact
trivia question
```

### Security Tools
```
generate password 20
hash hello
base64 encode MySecret
check password strength: P@ssw0rd!
```

### Analysis & Language
```
analyze sentiment: I love this project
summarize: [paste long text]
translate good morning to Tamil
supported languages
```

### Daily Briefing
```
good morning
morning briefing
daily briefing
```

---

## API Keys Setup

| Key | Where to Get | Required? |
|---|---|---|
| `ANTHROPIC_API_KEY` | https://console.anthropic.com | **Yes** (for full AI) |
| `OPENWEATHER_API_KEY` | https://openweathermap.org/api | Optional |
| `NEWS_API_KEY` | https://newsapi.org | Optional |

Without the Anthropic key, J.A.R.V.I.S. still works for all local commands but falls back to a basic response for complex AI questions.

---

## Running Without API Keys

All of the following work **without any API key**:
- Time, Date queries
- All System Commands (open/close apps, screenshot, volume, lock)
- Web Actions (open websites, Google search)
- Calculator and unit converter
- Notes, Tasks, Reminders (full CRUD)
- Jokes, Quotes, Fun Facts, Trivia (built-in)
- Security Tools (password generator, hash, base64)
- Sentiment Analysis (TextBlob — local)
- System Stats dashboard (psutil — local)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│        PRESENTATION LAYER (Browser)              │
│  Iron Man HUD · Socket.IO Client · Web Speech   │
└──────────────────┬──────────────────────────────┘
                   │  WebSocket + HTTP REST
┌──────────────────▼──────────────────────────────┐
│        APPLICATION LAYER (Python / Flask)         │
│  app.py · Intent Router · 18 Modules · Threads  │
│  ┌─────────────┐  ┌───────────────┐             │
│  │ Local Intent│  │  Claude Sonnet│             │
│  │  Detector   │→ │  AI Fallback  │             │
│  └─────────────┘  └───────────────┘             │
└──────────────────┬──────────────────────────────┘
                   │  sqlite3
┌──────────────────▼──────────────────────────────┐
│          DATA LAYER (SQLite — jarvis.db)          │
│   logs · notes · tasks · reminders · settings   │
└─────────────────────────────────────────────────┘
```

---

## License

This project is submitted as a final-year BCA academic project at  
Prof. Dhanapalan College of Science and Management, Kelambakkam.

© 2025 Nasreen Fathima S — All rights reserved.
