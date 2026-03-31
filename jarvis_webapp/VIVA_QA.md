# J.A.R.V.I.S. — Viva Question & Answer Guide
### Nasreen Fathima S · Reg No: 212300358

---

## Section 1: Project Introduction

**Q1. Tell me about your project.**

A: My project is J.A.R.V.I.S. — Just A Rather Very Intelligent System. It is a full-stack AI-powered personal assistant web application built with Python, Flask, and the Claude AI model from Anthropic. The system allows users to interact through both voice and text commands to perform a wide range of tasks — opening applications, managing notes and tasks, fetching news and weather, performing calculations, and having intelligent conversations. The frontend displays a real-time Iron Man HUD interface that shows live CPU, RAM, and disk statistics updating every two seconds via WebSocket.

---

**Q2. Why did you choose this topic?**

A: I chose this topic because it combines multiple areas of computer science that are highly relevant today — AI and language models, real-time web communication, system automation, and full-stack web development. Instead of building a simple CRUD application, this project demonstrates the integration of an actual AI API, live WebSocket communication, operating-system-level control, and a polished user interface. It is also inspired by the fictional J.A.R.V.I.S. from Iron Man, which made it an interesting and motivating challenge to build a real-world equivalent.

---

**Q3. What is the main purpose of J.A.R.V.I.S.?**

A: The main purpose is to provide a unified personal assistant that replaces the need to open multiple separate applications. Instead of manually opening a calculator, a notepad, a browser, and checking system info separately, J.A.R.V.I.S. handles all of these through a single voice or text interface. It also serves as a demonstration of AI integration — showing how a modern language model can be embedded into a real application to handle complex, open-ended queries.

---

## Section 2: Technology Questions

**Q4. Why did you use Flask instead of Django?**

A: Flask is a micro-framework, which means it has no mandatory project structure and minimal built-in features — you only add what you need. This makes it ideal for a project like J.A.R.V.I.S. where the focus is on custom business logic rather than a content management system or ORM. Django is better suited for large database-driven applications. Flask also integrates very cleanly with Flask-SocketIO, which is essential for the real-time WebSocket communication in this project.

---

**Q5. What is WebSocket and why did you use it instead of HTTP?**

A: HTTP is a request-response protocol — the browser sends a request and the server responds, then the connection closes. For a personal assistant, this has two major problems: first, every command would require a new connection setup which adds latency; second, the server cannot proactively push data to the browser without the browser asking for it. WebSocket solves both problems by keeping a persistent bidirectional connection open. In J.A.R.V.I.S., this allows the server to push real-time system stats every two seconds and fire reminder alerts the moment they are due — without the browser ever making a request.

---

**Q6. What is Flask-SocketIO?**

A: Flask-SocketIO is a Flask extension that adds Socket.IO protocol support. Socket.IO is built on top of WebSocket but adds features like automatic reconnection, fallback to long-polling for older browsers, and room-based message routing. In the code, I use `@socketio.on('command')` to handle incoming command events and `emit('response', data)` to send results back to the client. Background threads use `socketio.emit()` to push system stats to all connected clients.

---

**Q7. What is Claude Sonnet and how do you use it?**

A: Claude Sonnet (model ID: `claude-sonnet-4-20250514`) is a large language model from Anthropic. I access it via their REST API by sending an HTTP POST request to `https://api.anthropic.com/v1/messages`. Each request includes a system prompt that configures the AI to behave as J.A.R.V.I.S. — British tone, addressing the user as "sir" — and the full conversation history so it has context. The response is extracted from the `content[0].text` field of the JSON response and returned to the user. Conversation memory is maintained in a Python list of `{"role": "user/assistant", "content": "..."}` dictionaries, keeping the last 10 exchanges.

---

**Q8. What is Jaccard Similarity? How does the intent detector work?**

A: Jaccard similarity is a mathematical measure of how similar two sets are. It is calculated as the size of the intersection divided by the size of the union. In my intent detector, I tokenise both the user's input and each known command pattern into sets of words. For example, if the user says "open the chrome browser" and a known pattern is "open chrome", the intersection is {open, chrome} (size 2) and the union is {open, the, chrome, browser} (size 4), giving a similarity of 0.5. If this score is above my configured threshold of 0.35, the match is used. This approach is fast because it only uses simple set operations with no neural network computation.

---

**Q9. Why did you use SQLite instead of MySQL or PostgreSQL?**

A: J.A.R.V.I.S. is a single-user personal assistant running on a local machine, so there is no need for a separate database server process. SQLite is embedded directly into Python through the standard library `sqlite3` module — no installation, no configuration, no server to start. The entire database is a single file (`data/jarvis.db`) that is automatically created on first run. For a project that needs to store notes, tasks, and reminders locally without external dependencies, SQLite is the ideal choice.

---

**Q10. What is psutil and how do you use it?**

A: psutil (Process and System Utilities) is a Python library for retrieving information on running processes and system resource utilisation. I use it to collect CPU percentage (`psutil.cpu_percent()`), RAM usage (`psutil.virtual_memory()`), disk usage (`psutil.disk_usage('/')`), network I/O counters (`psutil.net_io_counters()`), and battery status (`psutil.sensors_battery()`). These are collected in a background daemon thread every 2 seconds and emitted to the browser via WebSocket so the HUD displays live statistics.

---

**Q11. What is TextBlob and how is it used?**

A: TextBlob is a Python library for processing textual data. Its `TextBlob(text).sentiment` property returns a `polarity` score (−1.0 to +1.0) and a `subjectivity` score (0.0 to 1.0). Polarity above 0.1 is classified as Positive, below −0.1 as Negative, and between the two as Neutral. I use this in the sentiment analysis module — when a user says "analyze sentiment: I love this project", TextBlob processes the text and returns the emotional tone, which J.A.R.V.I.S. then explains to the user.

---

**Q12. What is the Web Speech API?**

A: The Web Speech API is a browser-native JavaScript API for speech recognition and synthesis. The `SpeechRecognition` interface captures audio from the microphone and converts it to text — this is the speech-to-text (STT) part. The `SpeechSynthesis` interface reads text aloud using the device's built-in TTS voices — this provides the voice output. Both are available in Chrome and Edge without any additional libraries or server-side processing. In J.A.R.V.I.S., the recognised text is sent to the Flask server via WebSocket just like a typed command, so the server handles it identically.

---

## Section 3: Architecture & Design

**Q13. Explain the architecture of your project.**

A: J.A.R.V.I.S. follows a three-tier architecture. The first tier is the Presentation Layer — the browser-based Iron Man HUD frontend built with HTML, CSS, and JavaScript. The second tier is the Application Layer — the Python Flask server with Flask-SocketIO handling all business logic through 18 specialised modules. The third tier is the Data Layer — an SQLite database with 5 tables. The frontend and backend communicate via WebSocket for real-time command processing and system stats, and via HTTP REST API for CRUD operations on notes, tasks, and reminders. The backend communicates with external services — Claude AI, OpenWeather, NewsAPI, and Wikipedia — via HTTPS.

---

**Q14. How does the command routing work?**

A: The `process_command()` function in `app.py` uses a cascaded if-elif structure. It first checks for time/date patterns, then weather, then system commands like open/close, then web actions, then productivity commands for notes/tasks/reminders, then calculator and unit conversion, then translation, then news, then knowledge queries, then entertainment, then security tools, then sentiment and summarisation, then file manager, then greetings. If none of these patterns match, it calls the CSV-based intent detector. If the detector's confidence is below 0.35, it falls back to the Claude AI module. This design ensures most common commands are handled instantly without any API call.

---

**Q15. What are the 5 database tables and what does each store?**

A:
- **logs**: Every command-response pair with detected intent, action type, and timestamp. Used for statistics and conversation history display.
- **notes**: User's saved notes with title, content, category, and pin status. Supports CRUD operations.
- **tasks**: To-do items with priority (high/medium/low) and completion tracking. Ordered by priority and creation time.
- **reminders**: Timed reminders with a `remind_at` timestamp. The background thread monitors this and fires alerts.
- **settings**: A key-value store for user preferences, stored as a key-value pair (key is the primary key).

---

**Q16. How do background threads work without blocking Flask?**

A: Flask-SocketIO is configured with `async_mode='threading'`, which means the SocketIO server uses Python's standard threading module rather than an async event loop. This allows me to start regular daemon threads for the stats loop and reminder loop. Inside these threads, I call `socketio.emit()` directly to push data to all connected clients. Because they are daemon threads, they terminate automatically when the main process exits. The threading model is appropriate here because the background tasks are I/O-bound (reading psutil metrics and SQLite queries), not CPU-intensive.

---

## Section 4: Features & Code

**Q17. How does voice input work end-to-end?**

A: When the user clicks the microphone button, JavaScript calls `SpeechRecognition.start()`. The browser listens to the microphone and returns the recognised text in the `onresult` event handler. The JavaScript code then takes this text and emits it to the Flask server as a `command` WebSocket event — exactly the same event that a typed command would send. The server processes it identically through `process_command()`. After the response is received via the `response` WebSocket event, JavaScript creates a new `SpeechSynthesisUtterance` with a British English voice and calls `speechSynthesis.speak()`. After speaking finishes, the code automatically restarts `SpeechRecognition.start()` so the system continues listening in a loop.

---

**Q18. How is conversation memory implemented?**

A: In the `AIChat` class in `modules/ai_chat.py`, I maintain a Python list called `self.history`. Every user message is appended as `{"role": "user", "content": user_input}` and every AI response is appended as `{"role": "assistant", "content": reply}`. When making the next API call, this full history list is sent in the `messages` parameter. To prevent the list from growing too large and exceeding the API token limit, I trim it to keep only the last 20 entries (10 exchanges). This gives the AI context for multi-turn conversations. The history is cleared when the user says "clear memory" or when the server restarts.

---

**Q19. How does the reminder system work?**

A: When a user adds a reminder (e.g., "remind me to drink water at 3 PM"), it is saved to the `reminders` table with a `remind_at` timestamp. A background daemon thread (`reminder_check_loop`) runs continuously and calls `reminder_manager.check_reminders_loop(socketio)` which wakes up every 30 seconds, queries the database for reminders where `remind_at` is in the past and `done = 0`, and for each matching reminder, calls `socketio.emit()` to send an alert event to the browser. The browser then displays a popup notification and marks the reminder as done via a PUT request to `/api/reminders/<id>`.

---

**Q20. What does the daily briefing command return?**

A: The `_daily_briefing()` function in `app.py` generates a multi-section morning report. It includes: a time-appropriate greeting (Good morning/afternoon/evening), the current date, the current time, the number of pending tasks from the database, the number of active reminders, the number of commands sent today (from the logs table), a top news headline from the news module (if available), and a motivational quote. All of this is assembled into a single formatted string and returned as one response.

---

## Section 5: Critical Thinking

**Q21. What are the limitations of your system?**

A:
- The Claude AI requires an internet connection and an API key with usage credits.
- Voice recognition accuracy depends on the microphone quality and background noise.
- The system is designed for a single user — there is no multi-user authentication.
- The SQLite database cannot handle high concurrent write loads — suitable for single-user, not a web service.
- System commands like opening applications are platform-specific — the code handles Windows and Linux/macOS differently.
- The sentiment analyser uses a simple TextBlob model which may be less accurate than a fine-tuned NLP model.

---

**Q22. What would you improve if you had more time?**

A: I would add user authentication so multiple people can use the same instance with separate data. I would replace SQLite with PostgreSQL to support concurrent access. I would integrate long-term memory using a vector database so J.A.R.V.I.S. remembers past conversations across sessions. I would also deploy it to the cloud (AWS or Railway) so it can run 24/7 and be accessed from any device. A custom wake-word detector would make the voice activation truly hands-free.

---

**Q23. What is the difference between the local intent detector and Claude AI?**

A: The local intent detector is fast (under 10ms), offline, and deterministic — it always returns the same result for the same input. But it can only handle commands that are already in the training dataset. Claude AI is slow (1–3 seconds), requires internet, and costs API credits — but it can answer any question, reason about complex topics, and maintain conversational context. The two-layer design gives the best of both: speed and reliability for common commands, intelligence and flexibility for everything else.

---

**Q24. Is your project secure?**

A: The API key is stored in a `.env` file and loaded via `python-dotenv`, keeping it out of the source code. The `.env` file is excluded from version control. The Flask `SECRET_KEY` is configured in the same way. The system runs locally and is not exposed to the internet by default, so there is no risk of unauthorised external access. The SQLite database is a local file with standard OS file permissions. For a production deployment, I would add HTTPS, rate limiting, input sanitisation, and proper user authentication.

---

## Section 6: Quick Reference

**Q. What does JARVIS stand for?**  
A: Just A Rather Very Intelligent System

**Q. What port does the application run on?**  
A: Port 5000 (configurable in .env)

**Q. How many modules does the project have?**  
A: 18 capability modules in the `modules/` directory, plus `core/` modules for database and intent detection

**Q. What AI model is used?**  
A: Claude Sonnet — model ID: `claude-sonnet-4-20250514`

**Q. What database does it use?**  
A: SQLite3 — stored as `data/jarvis.db`

**Q. How many database tables are there?**  
A: 5 tables: logs, notes, tasks, reminders, settings

**Q. What is the intent confidence threshold?**  
A: 0.35 (35%) — configured in `config/settings.py` as `INTENT_THRESHOLD`

**Q. How often do system stats update?**  
A: Every 2 seconds via background WebSocket emission

**Q. What browser is recommended?**  
A: Google Chrome (required for Web Speech API)

**Q. How do you start the application?**  
A: `python app.py` — opens at `http://localhost:5000`
