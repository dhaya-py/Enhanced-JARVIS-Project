# 🚀 JARVIS Quick Start Guide

## ⚡ 5-Minute Setup

### Step 1: Verify Python
```bash
python --version
# Should show Python 3.11 or higher
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**If PyAudio fails on Windows:**
Download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
```bash
pip install PyAudio‑0.2.14‑cp311‑cp311‑win_amd64.whl
```

### Step 3: Run Jarvis
```bash
python main.py
```

## 🎮 Using Jarvis

1. **Click START** in the GUI
2. **Wait for "Listening..."** status
3. **Speak your command** clearly
4. **Wait for response**

## 🗣️ Quick Commands

### Try These First
- "Open notepad"
- "What time is it"
- "Open youtube"
- "Help"

### System Control
- "Open calculator"
- "Close window"
- "Take screenshot"

### Web Actions
- "Search google for Python"
- "Open github"

### Information
- "What's the date"
- "Tell me about yourself"

## 🔧 Optional Setup

### Add OpenAI GPT Support
1. Copy `.env.template` to `.env`
2. Add your API key:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```
3. Restart Jarvis

### Enable Weather
1. Get free API key from: https://openweathermap.org/api
2. Add to `.env`:
   ```
   OPENWEATHER_API_KEY=your-key-here
   ```

## ❌ Common Issues

### "Microphone not found"
- Check microphone connection
- Check Windows privacy settings
- Run: `python -c "import speech_recognition as sr; sr.Microphone()"`

### "Module not found"
```bash
pip install --upgrade -r requirements.txt
```

### GUI doesn't open
- Check if tkinter is installed
- Windows: Usually built-in
- Linux: `sudo apt-get install python3-tk`

### Voice not working
- Check microphone in system settings
- Try `voice.test_microphone()` in Python console

## 📖 Full Documentation

See `README.md` for complete documentation.

## 🆘 Need Help?

1. Check `README.md` troubleshooting section
2. Review console output for errors
3. Enable debug mode in `.env`:
   ```
   DEBUG_MODE=True
   ```

---

**Ready to go! Say "Open calculator" to test.**
