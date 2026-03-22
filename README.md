# JARVIS - AI-Based Personal Assistant System

A production-ready desktop AI assistant built with Python, featuring voice interaction, intent detection, system automation, and advanced AI capabilities.

## 🎯 Project Overview

Jarvis is a modular, scalable AI personal assistant designed for Windows/Linux environments. It demonstrates practical implementation of artificial intelligence concepts using clean software engineering principles.

### Key Features

- 🎤 **Voice Interaction**: Speech recognition and text-to-speech
- 🧠 **Intent Detection**: Machine learning-based command understanding
- 💻 **System Control**: Open/close applications, system commands
- 🌐 **Web Actions**: Search, open websites, navigate web
- 📊 **Activity Logging**: SQLite database for interaction history
- 🤖 **GPT Integration**: OpenAI GPT fallback for complex queries
- 🎨 **Modern GUI**: Tkinter-based desktop interface
- 🔧 **Phase 02 Extensions**: Face auth, gesture control, automation

## 📁 Project Structure

```
jarvis_project/
├── main.py                     # Main entry point
├── requirements.txt            # Python dependencies
├── .env.template              # Environment variables template
├── config/
│   └── settings.py            # Configuration management
├── core/
│   ├── database.py            # SQLite database manager
│   ├── engine.py              # Main AI engine
│   ├── intent_detector.py    # Intent classification
│   └── voice_system.py        # Speech recognition & TTS
├── modules/
│   ├── gpt_integration.py     # OpenAI GPT integration
│   ├── information.py         # Info provider (time, date, weather)
│   ├── system_actions.py      # System-level operations
│   └── web_actions.py         # Web-related operations
├── gui/
│   └── main_window.py         # Tkinter GUI
├── data/
│   ├── os_dataset.csv         # Intent training data
│   └── jarvis.db              # SQLite database (auto-created)
└── phase02/                   # Advanced features
    ├── automation/
    │   └── controller.py      # Brightness/volume control
    ├── face_auth/
    │   └── authenticator.py   # Face recognition
    └── gesture/
        └── controller.py      # Hand gesture control
```

## 🚀 Installation

### Prerequisites

- **Python 3.11+** (Required)
- **Windows 10/11** or **Linux** (Tested on Ubuntu 24)
- **Microphone** (For voice input)
- **Speakers** (For voice output)
- **Webcam** (Optional, for Phase 02 features)

### Step 1: Clone/Extract Project

```bash
# Navigate to project directory
cd jarvis_project
```

### Step 2: Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

**Note for Windows PyAudio Installation:**
If PyAudio fails to install, download the wheel file:
```bash
# Download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# Then install:
pip install PyAudio‑0.2.14‑cp311‑cp311‑win_amd64.whl
```

### Step 3: Configure Environment (Optional)

```bash
# Copy template
cp .env.template .env

# Edit .env and add your API keys (optional)
# - OPENAI_API_KEY (for GPT integration)
# - OPENWEATHER_API_KEY (for weather)
```

**Note**: Jarvis works WITHOUT API keys using fallback responses.

## 🎮 Usage

### Running Jarvis

```bash
# Activate virtual environment first
python main.py
```

### GUI Controls

1. **START Button**: Activates Jarvis and begins listening
2. **STOP Button**: Deactivates Jarvis
3. **Clear Logs**: Clears activity log display

### Voice Commands

#### System Commands
- "Open notepad"
- "Open calculator"
- "Open chrome"
- "Close window"
- "Take screenshot"
- "Lock screen"

#### Web Actions
- "Open youtube"
- "Search google for [query]"
- "Open github"

#### Information
- "What time is it"
- "What's the date"
- "Get weather"
- "Who are you"
- "Help"

#### Control
- "Stop" (stops listening)
- "Exit" (closes Jarvis)

### Testing Without Microphone

For testing in environments without microphone access, you can modify the engine to accept text input instead of voice.

## 🔧 Configuration

### Environment Variables (.env)

```env
# OpenAI API (Optional)
OPENAI_API_KEY=sk-...

# Weather API (Optional)
OPENWEATHER_API_KEY=...

# System Settings
DEBUG_MODE=True
VOICE_TIMEOUT=5
```

### Intent Dataset

Add custom commands to `data/os_dataset.csv`:

```csv
command,intent,action_type
your command,your_intent,system
```

## 📦 Phase 02 Features

### Automation Control

```python
from phase02.automation.controller import automation

# Brightness control
automation.set_brightness(50)  # 0-100

# Volume control
automation.set_volume(75)  # 0-100
automation.mute_volume()
```

### Face Authentication

```python
from phase02.face_auth.authenticator import face_auth

# Register user
face_auth.capture_face("username", num_samples=5)

# Authenticate
authenticated, name = face_auth.authenticate()
```

### Gesture Control

```python
from phase02.gesture.controller import gesture_controller

# Start gesture control
gesture_controller.start_gesture_control()
```

## 🗄️ Database Schema

```sql
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    command TEXT NOT NULL,
    response TEXT NOT NULL,
    timestamp TEXT NOT NULL
);
```

## 🏗️ Architecture

### Execution Flow

```
User Input (Voice)
    ↓
Voice System (SpeechRecognition)
    ↓
Intent Detector (Scikit-learn)
    ↓
Engine Router
    ↓
Action Modules (System/Web/Info/GPT)
    ↓
Response Generator
    ↓
Voice Output (pyttsx3)
    ↓
Database Logger (SQLite)
```

### Design Principles

- **Modular Architecture**: Clear separation of concerns
- **Graceful Degradation**: Works without optional APIs
- **Thread Safety**: Engine runs in separate thread
- **Error Handling**: Comprehensive try-catch blocks
- **Restartable**: Engine can be started/stopped multiple times

## 🛠️ Troubleshooting

### Microphone Not Working
```python
# Test microphone
from core.voice_system import voice
voice.test_microphone()
```

### TTS Not Working
```python
# Test speakers
from core.voice_system import voice
voice.test_speakers()
```

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Database Errors
```bash
# Delete and recreate database
rm data/jarvis.db
python main.py  # Will auto-create
```

## 📊 System Requirements

### Minimum
- CPU: Dual-core 2.0 GHz
- RAM: 4 GB
- Storage: 500 MB
- OS: Windows 10 / Ubuntu 20.04

### Recommended
- CPU: Quad-core 2.5 GHz+
- RAM: 8 GB+
- Storage: 1 GB
- OS: Windows 11 / Ubuntu 24

## 🔐 Security Notes

- API keys stored in `.env` (not committed to git)
- Face encodings encrypted with pickle
- No data sent to external servers (except OpenAI if enabled)
- Local SQLite database for logs

## 🤝 Contributing

This is an academic project. For improvements:

1. Fork the repository
2. Create feature branch
3. Implement changes
4. Test thoroughly
5. Submit pull request

## 📄 License

Educational/Academic use only. See project documentation.

## 👥 Credits

**Project Guide**: [Guide Name]  
**Developer**: [Your Name]  
**Institution**: [Your College/University]  
**Year**: 2024-2025

## 📞 Support

For issues or questions:
- Check troubleshooting section
- Review code comments
- Contact project maintainer

## 🎓 Academic Notes

This project fulfills requirements for:
- Final year Computer Science project
- Demonstrates AI/ML implementation
- Shows software engineering practices
- Production-ready code quality
- Suitable for academic evaluation

---

**Built with ❤️ for academic excellence**



