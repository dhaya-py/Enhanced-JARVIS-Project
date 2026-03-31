# J.A.R.V.I.S. — Complete Setup Guide
### Step-by-step installation for local development and demo

---

## Prerequisites

Before starting, make sure you have:

| Requirement | Check Command | Required Version |
|---|---|---|
| Python | `python --version` | 3.10 or higher |
| pip | `pip --version` | Latest |
| Google Chrome | Open browser | Latest (for voice input) |
| Internet connection | — | Required for AI, news, weather |

---

## Step 1 — Extract the Project

```bash
# If you have the zip file:
unzip jarviswebapp-zip.zip
cd jarviswebapp-zip
```

Your folder structure should look like:
```
jarviswebapp-zip/
├── app.py
├── requirements.txt
├── .env.template
├── config/
├── core/
├── modules/
├── data/
├── templates/
└── static/
```

---

## Step 2 — Create a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt.

---

## Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all required packages:
- Flask, Flask-SocketIO, Flask-CORS
- anthropic (Claude AI)
- psutil, pyautogui
- TextBlob, SpeechRecognition, pyttsx3
- requests, wikipedia-api, python-dotenv
- eventlet

**If you get an error on PyAudio (Windows):**
```bash
pip install pipwin
pipwin install pyaudio
```

**If you get an error on PyAudio (Linux):**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

---

## Step 4 — Configure API Keys

```bash
# Copy the template
cp .env.template .env
```

Open `.env` in any text editor and fill in your keys:

```env
# Required for full AI conversation
ANTHROPIC_API_KEY=sk-ant-api03-...

# Optional — for live weather data
OPENWEATHER_API_KEY=your_key_here

# Optional — for live news headlines
NEWS_API_KEY=your_key_here

# Application settings (defaults are fine)
DEBUG_MODE=False
SECRET_KEY=jarvis-iron-man-2024
HOST=0.0.0.0
PORT=5000
```

### Where to Get API Keys

| API | Registration URL | Free Tier |
|---|---|---|
| Anthropic Claude | https://console.anthropic.com | Yes (limited credits) |
| OpenWeather | https://openweathermap.org/api | Yes (1000 calls/day) |
| NewsAPI | https://newsapi.org | Yes (100 requests/day) |

> **Note:** The application runs without any API keys. Local features (system commands, calculator, notes, tasks, reminders, jokes, quotes, security tools, sentiment analysis, system stats) all work offline. Only AI chat, weather, and news require API keys.

---

## Step 5 — Run the Application

```bash
python app.py
```

You should see output like:
```
══════════════════════════════════════════════════════════════
  ░░░░  J.A.R.V.I.S. AI COMMAND CENTER  ░░░░
  Version 3.0 — Flask + SocketIO + AI
  Running at: http://localhost:5000
══════════════════════════════════════════════════════════════
[IntentDetector] Loaded 150 patterns
```

---

## Step 6 — Open in Browser

Open **Google Chrome** (recommended) and navigate to:

```
http://localhost:5000
```

The Iron Man HUD interface should load with:
- Animated arc reactor in the centre
- Command input box at the bottom
- System stats panels on the sides
- News ticker at the top

---

## Testing the Installation

Try these commands in order to verify everything works:

```
what time is it?          ← Tests local routing (no API needed)
system info               ← Tests psutil system monitoring
good morning              ← Tests daily briefing
add note: Test note       ← Tests SQLite notes
show my notes             ← Tests database retrieval
tell me a joke            ← Tests entertainment module
generate password 16      ← Tests security tools
what is artificial intelligence?  ← Tests Claude AI (requires key)
```

---

## Voice Input Setup

1. Open the application in **Google Chrome** (Chrome only — Firefox does not support Web Speech API)
2. Click the **microphone button** or the **arc reactor**
3. Allow microphone access when Chrome prompts you
4. Speak clearly: *"What time is it?"*
5. J.A.R.V.I.S. should respond and speak the answer aloud

> **Tip:** Use Chrome. Safari has limited support and Firefox does not support Web Speech API.

---

## Accessing the REST API

The application exposes REST endpoints you can test in your browser or with Postman:

| URL | Description |
|---|---|
| `http://localhost:5000/api/logs` | All interaction logs |
| `http://localhost:5000/api/stats` | Command and data counts |
| `http://localhost:5000/api/notes` | All saved notes |
| `http://localhost:5000/api/tasks` | All tasks |
| `http://localhost:5000/api/reminders` | All reminders |
| `http://localhost:5000/api/news?category=tech` | Live tech news |
| `http://localhost:5000/api/system/info` | Detailed system info |

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again |
| `Address already in use` | Port 5000 is occupied. Change `PORT=5001` in `.env` |
| Voice not working | Use Google Chrome; check microphone permissions in browser settings |
| `APIConnectionError` | Check `ANTHROPIC_API_KEY` in `.env`; check internet connection |
| SQLite errors | Delete `data/jarvis.db` — it will be recreated automatically |
| `PyAudio not found` | See PyAudio installation instructions above (platform-specific) |
| Page loads but stats don't update | WebSocket blocked by firewall — try `http://127.0.0.1:5000` |

---

## Stopping the Server

Press `Ctrl + C` in the terminal where `python app.py` is running.

---

## Project Files Reference

| File | Purpose |
|---|---|
| `app.py` | Main server: routes, WebSocket events, command dispatcher |
| `config/settings.py` | All configuration values (API keys, model, port, thresholds) |
| `core/database.py` | SQLite DatabaseManager class |
| `core/intent_detector.py` | CSV-based intent classifier |
| `data/os_dataset.csv` | Intent training data (command → intent → action_type) |
| `data/jarvis.db` | SQLite database file (auto-created) |
| `templates/index.html` | Single-page frontend (HUD interface) |
| `static/css/jarvis.css` | Iron Man HUD styles |
| `static/js/jarvis.js` | Client-side Socket.IO, voice, TTS, panel logic |
| `.env` | API keys and configuration (do not commit to Git) |
| `.env.template` | Template for .env file |
| `requirements.txt` | All Python dependencies |
