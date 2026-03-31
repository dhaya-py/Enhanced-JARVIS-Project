"""
J.A.R.V.I.S. — Flask + SocketIO Web Command Center
Main application server
"""
import os
import sys
import threading
import time
import re
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

from config.settings import config
from core.database import db
from core.intent_detector import intent_detector
from modules.ai_chat import ai_chat
from modules.information import info_provider
from modules.system_actions import system_actions
from modules.web_actions import web_actions
from modules.calculator import smart_calculator
from modules.entertainment import entertainment
from modules.knowledge import knowledge_base
from modules.news import news_fetcher
from modules.notes import notes_manager
from modules.planner import task_planner
from modules.reminders import reminder_manager
from modules.sentiment import sentiment_analyzer
from modules.summarizer import text_summarizer
from modules.translator import translator
from modules.security_tools import security_tools
from modules.file_manager import file_manager
from modules.voice_engine import voice_engine

try:
    import psutil
    PSUTIL_OK = True
except ImportError:
    PSUTIL_OK = False

# ── App Setup ────────────────────────────────────────────────────────────────

app = Flask(__name__,
            template_folder="templates",
            static_folder="static")
app.config["SECRET_KEY"] = config.SECRET_KEY
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading", logger=False, engineio_logger=False)

# ── Background: System Stats ─────────────────────────────────────────────────

def system_stats_loop():
    while True:
        try:
            if PSUTIL_OK:
                cpu = psutil.cpu_percent(interval=1)
                mem = psutil.virtual_memory()
                disk_path = "C:\\" if sys.platform == "win32" else "/"
                disk = psutil.disk_usage(disk_path)
                net = psutil.net_io_counters()
                battery = psutil.sensors_battery()
                stats = {
                    "cpu": cpu,
                    "ram": mem.percent,
                    "ram_used": round(mem.used / 1024**3, 1),
                    "ram_total": round(mem.total / 1024**3, 1),
                    "disk": disk.percent,
                    "disk_free": round(disk.free / 1024**3, 1),
                    "net_sent": round(net.bytes_sent / 1024**2, 1),
                    "net_recv": round(net.bytes_recv / 1024**2, 1),
                    "battery": round(battery.percent, 1) if battery else None,
                    "plugged": battery.power_plugged if battery else None,
                }
            else:
                import random
                stats = {
                    "cpu": round(random.uniform(10, 45), 1),
                    "ram": round(random.uniform(40, 75), 1),
                    "ram_used": round(random.uniform(4, 8), 1),
                    "ram_total": 16,
                    "disk": 55,
                    "disk_free": 250,
                    "net_sent": 12.4,
                    "net_recv": 34.1,
                    "battery": None,
                    "plugged": None,
                }
            socketio.emit("system_stats", stats)
        except Exception as e:
            pass
        time.sleep(2)

# ── Background: Reminders ────────────────────────────────────────────────────

def reminder_check_loop():
    reminder_manager.check_reminders_loop(socketio)

# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/logs")
def api_logs():
    logs = db.get_recent_logs(int(request.args.get("limit", 50)))
    return jsonify({"success": True, "data": logs})

@app.route("/api/logs/clear", methods=["POST"])
def api_logs_clear():
    db.clear_logs()
    return jsonify({"success": True})

@app.route("/api/stats")
def api_stats():
    return jsonify({"success": True, "data": db.get_stats()})

@app.route("/api/notes", methods=["GET", "POST"])
def api_notes():
    if request.method == "GET":
        return jsonify({"success": True, "data": db.get_all_notes()})
    d = request.json or {}
    note = db.add_note(d.get("title", "Untitled"), d.get("content", ""), d.get("category", "general"))
    return jsonify({"success": True, "data": note})

@app.route("/api/notes/<int:note_id>", methods=["PUT", "DELETE"])
def api_note(note_id):
    if request.method == "DELETE":
        db.delete_note(note_id)
        return jsonify({"success": True})
    d = request.json or {}
    db.update_note(note_id, d.get("title"), d.get("content"))
    return jsonify({"success": True})

@app.route("/api/tasks", methods=["GET", "POST"])
def api_tasks():
    if request.method == "GET":
        return jsonify({"success": True, "data": db.get_all_tasks()})
    d = request.json or {}
    task = db.add_task(d.get("title", ""), d.get("priority", "medium"))
    return jsonify({"success": True, "data": task})

@app.route("/api/tasks/<int:task_id>", methods=["PUT", "DELETE"])
def api_task(task_id):
    if request.method == "DELETE":
        db.delete_task(task_id)
        return jsonify({"success": True})
    db.toggle_task(task_id)
    return jsonify({"success": True})

@app.route("/api/reminders", methods=["GET", "POST"])
def api_reminders():
    if request.method == "GET":
        return jsonify({"success": True, "data": db.get_all_reminders()})
    d = request.json or {}
    rem = db.add_reminder(d.get("text", ""), d.get("remind_at"))
    return jsonify({"success": True, "data": rem})

@app.route("/api/reminders/<int:rem_id>", methods=["PUT", "DELETE"])
def api_reminder(rem_id):
    if request.method == "DELETE":
        db.delete_reminder(rem_id)
        return jsonify({"success": True})
    db.mark_reminder_done(rem_id)
    return jsonify({"success": True})

@app.route("/api/news")
def api_news():
    cat = request.args.get("category", "tech")
    return jsonify({"success": True, "data": news_fetcher.get_news(cat, 6)})

@app.route("/api/system/info")
def api_system_info():
    return jsonify({"success": True, "data": system_actions.get_system_info()})

# ── WebSocket: Core ──────────────────────────────────────────────────────────

@socketio.on("connect")
def on_connect():
    emit("connected", {"msg": "J.A.R.V.I.S. online", "ts": datetime.now().strftime("%H:%M:%S")})

@socketio.on("command")
def on_command(data):
    text = (data.get("text") or "").strip()
    if not text:
        return
    emit("status", {"state": "processing", "msg": "Processing..."})
    try:
        response, intent, action_type, open_url = process_command(text)
        db.log_interaction(text, response, intent, action_type)
        emit("response", {
            "text": response,
            "command": text,
            "intent": intent,
            "action_type": action_type,
            "open_url": open_url,
            "ts": datetime.now().strftime("%H:%M:%S"),
        })
    except Exception as e:
        emit("response", {"text": f"Error: {e}", "command": text, "ts": datetime.now().strftime("%H:%M:%S")})
    emit("status", {"state": "ready", "msg": "Ready"})

@socketio.on("clear_memory")
def on_clear_memory():
    msg = ai_chat.clear_history()
    emit("response", {"text": msg, "ts": datetime.now().strftime("%H:%M:%S")})

@socketio.on("get_news_ticker")
def on_news_ticker():
    items = news_fetcher.get_all_for_ticker()
    emit("news_ticker", {"items": items})

# ── Command Processor ────────────────────────────────────────────────────────

def process_command(cmd: str):
    """
    Returns (response_text, intent, action_type, open_url_or_None)
    """
    low = cmd.lower().strip()
    open_url = None

    # ── Clear conversation memory ──────────────────────────────────
    if low in ("clear memory", "forget", "reset memory", "new conversation"):
        return ai_chat.clear_history(), "clear_memory", "control", None

    # ── Time / Date ────────────────────────────────────────────────
    if any(p in low for p in ("what time", "current time", "tell me the time", "what's the time")):
        return info_provider.get_time(), "get_time", "info", None
    if any(p in low for p in ("what date", "today's date", "what day", "tell me the date")):
        return info_provider.get_date(), "get_date", "info", None
    if "date and time" in low or "datetime" in low:
        return info_provider.get_datetime(), "get_datetime", "info", None

    # ── Weather ────────────────────────────────────────────────────
    if any(p in low for p in ("weather", "temperature", "forecast", "how hot", "how cold")):
        city_m = re.search(r'(?:in|for|at)\s+([A-Za-z\s]+)$', low)
        city = city_m.group(1).strip().title() if city_m else "Chennai"
        return info_provider.get_weather(city), "get_weather", "info", None

    # ── About / Help ───────────────────────────────────────────────
    if any(p in low for p in ("who are you", "what are you", "about jarvis", "tell me about yourself")):
        return info_provider.get_about_jarvis(), "about", "info", None
    if any(p in low for p in ("help", "what can you do", "commands", "capabilities")):
        return info_provider.get_help(), "help", "info", None

    # ── System Actions ─────────────────────────────────────────────
    if low.startswith(("open ", "launch ", "start ")):
        app_name = re.sub(r'^(open|launch|start)\s+', '', low).strip()
        # Check if it's a website first
        for site in web_actions.SITE_MAP:
            if site in app_name:
                ok, msg, url = web_actions.open_website(site)
                return msg, "open_website", "web", url
        ok, msg = system_actions.open_application(app_name)
        return msg, f"open_{app_name}", "system", None

    if low.startswith("close "):
        app_name = low.replace("close ", "").strip()
        ok, msg = system_actions.close_application(app_name)
        return msg, f"close_{app_name}", "system", None

    if any(p in low for p in ("screenshot", "capture screen", "take a screenshot")):
        ok, msg = system_actions.take_screenshot()
        return msg, "screenshot", "system", None

    if any(p in low for p in ("lock screen", "lock computer", "lock the screen")):
        ok, msg = system_actions.lock_screen()
        return msg, "lock_screen", "system", None

    if "shutdown" in low or "shut down" in low:
        ok, msg = system_actions.shutdown_system()
        return msg, "shutdown", "system", None

    if "restart" in low or "reboot" in low:
        ok, msg = system_actions.restart_system()
        return msg, "restart", "system", None

    if "cancel shutdown" in low:
        ok, msg = system_actions.cancel_shutdown()
        return msg, "cancel_shutdown", "system", None

    if any(p in low for p in ("sleep", "suspend")):
        ok, msg = system_actions.sleep_system()
        return msg, "sleep", "system", None

    m_vol = re.search(r'(?:set\s+)?volume\s+(?:to\s+)?(\d+)', low)
    if m_vol:
        ok, msg = system_actions.set_volume(int(m_vol.group(1)))
        return msg, "set_volume", "system", None
    if "volume up" in low or "increase volume" in low:
        ok, msg = system_actions.set_volume(80)
        return msg, "vol_up", "system", None
    if "volume down" in low or "decrease volume" in low or "lower volume" in low:
        ok, msg = system_actions.set_volume(30)
        return msg, "vol_down", "system", None

    if "list processes" in low or "running processes" in low or "top processes" in low:
        return system_actions.list_processes(), "list_processes", "system", None

    if "system info" in low or "system status" in low or "pc info" in low:
        info = system_actions.get_system_info()
        txt = (f"System Info, sir:\n"
               f"OS: {info.get('os','')} {info.get('os_version','')}\n"
               f"CPU: {info.get('cpu_percent',0):.1f}% ({info.get('cpu_count',0)} cores @ {info.get('cpu_freq',0)} MHz)\n"
               f"RAM: {info.get('memory_used',0)} GB / {info.get('memory_total',0)} GB ({info.get('memory_percent',0):.1f}%)\n"
               f"Disk: {info.get('disk_used',0)} GB / {info.get('disk_total',0)} GB ({info.get('disk_percent',0):.1f}%)")
        if info.get("battery"):
            txt += f"\nBattery: {info['battery']}% {'(Plugged)' if info.get('plugged') else '(On Battery)'}"
        return txt, "system_info", "system", None

    # ── Web Actions ────────────────────────────────────────────────
    m_search = re.search(r'(?:search\s+(?:google\s+)?for|google|look\s+up|search)\s+(.+)', low)
    if m_search:
        query = m_search.group(1).strip()
        ok, msg, url = web_actions.google_search(query)
        return msg, "google_search", "web", url

    m_yt = re.search(r'(?:search\s+youtube\s+for|youtube\s+search)\s+(.+)', low)
    if m_yt:
        ok, msg, url = web_actions.youtube_search(m_yt.group(1).strip())
        return msg, "youtube_search", "web", url

    for site_name in web_actions.SITE_MAP:
        if site_name in low:
            ok, msg, url = web_actions.open_website(site_name)
            return msg, f"open_{site_name}", "web", url

    # ── Notes ──────────────────────────────────────────────────────
    if any(p in low for p in ("add note", "save note", "note down", "write note", "make a note")):
        text = re.sub(r'^(add note|save note|note down|write note|make a note)\s*:?\s*', '', low).strip()
        return notes_manager.add_note_quick(text), "add_note", "productivity", None
    if any(p in low for p in ("show notes", "my notes", "list notes", "read my notes")):
        return notes_manager.get_notes_text(), "show_notes", "productivity", None
    m_note_search = re.search(r'(?:search|find)\s+notes?\s+(.+)', low)
    if m_note_search:
        return notes_manager.search_notes(m_note_search.group(1)), "search_notes", "productivity", None

    # ── Tasks ──────────────────────────────────────────────────────
    if any(p in low for p in ("add task", "new task", "todo", "to do")):
        text = re.sub(r'^(add task|new task|todo|to do)\s*:?\s*', '', low).strip()
        return task_planner.add_task_quick(text), "add_task", "productivity", None
    if any(p in low for p in ("show tasks", "my tasks", "list tasks", "pending tasks", "task list")):
        return task_planner.get_tasks_text(), "show_tasks", "productivity", None

    # ── Reminders ──────────────────────────────────────────────────
    if any(p in low for p in ("remind me", "set reminder", "add reminder")):
        text = re.sub(r'^(remind me|set reminder|add reminder)\s*:?\s*(to\s+)?', '', low).strip()
        return reminder_manager.add_reminder_quick(text), "add_reminder", "productivity", None
    if any(p in low for p in ("show reminders", "my reminders", "list reminders")):
        return reminder_manager.get_reminders_text(), "show_reminders", "productivity", None

    # ── Calculator ─────────────────────────────────────────────────
    if any(p in low for p in ("calculate", "calc ", "compute", "solve", "what is ")) and \
       any(c in low for c in "+-*/^%√"):
        expr = re.sub(r'^(calculate|calc|compute|solve|what is)\s+', '', low)
        return smart_calculator.calculate(expr), "calculate", "utility", None

    m_conv = re.search(r'([\d.]+)\s+(\w+)\s+(?:to|in|into)\s+(\w+)', low)
    if m_conv or ("convert" in low and " to " in low):
        return smart_calculator.convert(low), "convert", "utility", None

    # ── Translation ────────────────────────────────────────────────
    if any(p in low for p in ("translate", "say in", "how to say", "say this in")):
        return translator.translate(low), "translate", "utility", None
    if "supported languages" in low or "what languages" in low:
        return translator.get_supported_languages(), "languages", "utility", None

    # ── News ───────────────────────────────────────────────────────
    if any(p in low for p in ("news", "headlines", "latest news", "whats happening", "what's happening")):
        cat = "tech"
        for c in ("tech", "science", "world", "sports", "business"):
            if c in low:
                cat = c
                break
        return news_fetcher.get_news_text(cat), "get_news", "info", None

    # ── Knowledge ──────────────────────────────────────────────────
    if any(p in low for p in ("who is ", "who was ", "what is ", "tell me about ", "define ", "explain ")):
        query = re.sub(r'^(who is|who was|what is|tell me about|define|explain)\s+', '', low)
        if len(query) > 2:
            return knowledge_base.search(query), "knowledge", "info", None

    # ── Entertainment ──────────────────────────────────────────────
    if any(p in low for p in ("tell me a joke", "joke", "make me laugh", "say something funny")):
        return entertainment.get_joke(), "joke", "fun", None
    if any(p in low for p in ("quote", "motivate me", "inspiration", "motivational quote", "wise words")):
        return entertainment.get_quote(), "quote", "fun", None
    if any(p in low for p in ("fun fact", "interesting fact", "did you know", "tell me something interesting")):
        return entertainment.get_fun_fact(), "fun_fact", "fun", None
    if any(p in low for p in ("trivia", "quiz me", "quiz question")):
        return entertainment.get_trivia(), "trivia", "fun", None

    # ── Security Tools ─────────────────────────────────────────────
    m_pwd = re.search(r'(?:generate\s+)?password(?:\s+(\d+))?', low)
    if m_pwd and any(p in low for p in ("generate password", "create password", "random password", "make password")):
        length = int(m_pwd.group(1)) if m_pwd.group(1) else 16
        return security_tools.generate_password(length), "generate_password", "security", None

    if "hash " in low:
        text = re.sub(r'.*(hash\s+)', '', low).strip()
        return security_tools.hash_text(text), "hash", "security", None

    if "base64 encode" in low:
        text = low.replace("base64 encode", "").strip()
        return security_tools.encode_base64(text), "base64_encode", "security", None
    if "base64 decode" in low:
        text = low.replace("base64 decode", "").strip()
        return security_tools.decode_base64(text), "base64_decode", "security", None

    if "check password" in low or "password strength" in low:
        text = re.sub(r'(check\s+)?password(\s+strength)?(\s+of)?\s+', '', low).strip()
        return security_tools.check_password_strength(text), "check_password", "security", None

    # ── Sentiment / Summarize ──────────────────────────────────────
    if any(p in low for p in ("analyze sentiment", "sentiment of", "sentiment analysis", "how does this feel")):
        text = re.sub(r'^(analyze sentiment|sentiment of|sentiment analysis|how does this feel)\s*:?\s*', '', cmd).strip()
        return sentiment_analyzer.analyze(text), "sentiment", "analysis", None

    if any(p in low for p in ("summarize", "summary of", "tldr", "give me a summary")):
        text = re.sub(r'^(summarize|summary of|tldr|give me a summary)\s*:?\s*', '', cmd).strip()
        return text_summarizer.summarize(text), "summarize", "analysis", None

    # ── File Manager ───────────────────────────────────────────────
    if any(p in low for p in ("find file", "search file", "locate file")):
        fname = re.sub(r'^(find file|search file|locate file)\s+', '', low).strip()
        return file_manager.search_files(fname), "find_file", "system", None

    if "disk usage" in low or "disk space" in low:
        return file_manager.get_disk_usage(), "disk_usage", "system", None

    if any(p in low for p in ("list files", "list directory", "show files")):
        return file_manager.list_directory(), "list_dir", "system", None

    # ── Daily Briefing ─────────────────────────────────────────────
    if any(p in low for p in ("briefing", "daily briefing", "morning briefing", "good morning")):
        return _daily_briefing(), "briefing", "info", None

    # ── Greetings ──────────────────────────────────────────────────
    if any(p in low for p in ("hello", "hi jarvis", "hey jarvis", "greetings")):
        import random
        greets = [
            "Good day, sir. How may I assist you?",
            "Hello, sir. All systems are operational. What do you need?",
            "Greetings. J.A.R.V.I.S. at your service, sir.",
        ]
        return random.choice(greets), "greeting", "social", None

    if any(p in low for p in ("thank you", "thanks", "good job", "well done", "great")):
        return info_provider.acknowledge(), "acknowledge", "social", None

    if low in ("stop", "goodbye", "bye", "exit", "quit", "standby"):
        return "J.A.R.V.I.S. entering standby mode, sir. Call me when you need me.", "exit", "control", None

    # ── Intent Detector fallback ───────────────────────────────────
    intent, action_type, confidence = intent_detector.detect_intent(cmd)
    if intent and confidence >= config.INTENT_THRESHOLD:
        return _dispatch_intent(intent, action_type, cmd)

    # ── AI Chat (final fallback) ───────────────────────────────────
    return ai_chat.get_response(cmd), "ai_chat", "ai", None


def _dispatch_intent(intent: str, action_type: str, cmd: str):
    if action_type == "system":
        if intent.startswith("open_"):
            app_name = intent.replace("open_", "")
            ok, msg = system_actions.open_application(app_name)
            return msg, intent, action_type, None
        if intent.startswith("close_"):
            app_name = intent.replace("close_", "")
            ok, msg = system_actions.close_application(app_name)
            return msg, intent, action_type, None
        if intent == "take_screenshot":
            ok, msg = system_actions.take_screenshot()
            return msg, intent, action_type, None
    if action_type == "web":
        if intent.startswith("open_"):
            site = intent.replace("open_", "")
            ok, msg, url = web_actions.open_website(site)
            return msg, intent, action_type, url
        if intent == "google_search":
            query = re.sub(r'search\s+(google\s+)?for\s+|search\s+|google\s+', '', cmd, flags=re.I).strip()
            ok, msg, url = web_actions.google_search(query)
            return msg, intent, action_type, url
    if action_type == "info":
        if intent == "get_time": return info_provider.get_time(), intent, action_type, None
        if intent == "get_date": return info_provider.get_date(), intent, action_type, None
        if intent == "get_weather": return info_provider.get_weather(), intent, action_type, None
        if intent == "about_jarvis": return info_provider.get_about_jarvis(), intent, action_type, None
        if intent == "show_help": return info_provider.get_help(), intent, action_type, None
        if intent == "acknowledge": return info_provider.acknowledge(), intent, action_type, None
    if action_type == "control":
        return "J.A.R.V.I.S. acknowledged, sir.", intent, action_type, None
    return ai_chat.get_response(cmd), "ai_chat", "ai", None


def _daily_briefing() -> str:
    now = datetime.now()
    hour = now.hour
    greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 17 else "Good evening"
    parts = [f"☀️ {greeting}, sir! Here is your daily briefing:\n"]
    parts.append(f"📅 {info_provider.get_date()}")
    parts.append(f"🕐 {info_provider.get_time()}")
    pending = db.get_pending_tasks_count()
    if pending:
        parts.append(f"📋 You have {pending} pending task(s) awaiting your attention.")
    active_rem = db.get_active_reminders_count()
    if active_rem:
        parts.append(f"🔔 {active_rem} active reminder(s) are set.")
    stats = db.get_stats()
    parts.append(f"💬 You have sent {stats['today_commands']} command(s) today.")
    try:
        headline = news_fetcher.get_headline()
        if headline:
            parts.append(f"📰 Top headline: {headline}")
    except Exception:
        pass
    parts.append(f"\n💡 {entertainment.get_quote_short()}")
    return "\n".join(parts)


# ── Startup ──────────────────────────────────────────────────────────────────

def start_server():
    print("=" * 62)
    print("  ░░░░  J.A.R.V.I.S. AI COMMAND CENTER  ░░░░")
    print("  Version 3.0 — Flask + SocketIO + AI")
    print(f"  Running at: http://localhost:{config.PORT}")
    print("=" * 62)

    # Background threads
    threading.Thread(target=system_stats_loop, daemon=True).start()
    threading.Thread(target=reminder_check_loop, daemon=True).start()

    def handle_voice_command(text):
        if not text.strip():
            return
        # Display spoken input on web UI
        socketio.emit("voice_recognized", {"text": text})
        socketio.emit("status", {"state": "processing", "msg": "Listening/Processing..."})
        try:
            response, intent, action_type, open_url = process_command(text)
            db.log_interaction(text, response, intent, action_type)
            socketio.emit("response", {
                "text": response,
                "command": text,
                "intent": intent,
                "action_type": action_type,
                "open_url": open_url,
                "ts": datetime.now().strftime("%H:%M:%S"),
            })
        except Exception as e:
            print(f"[VoiceCommand Error] {e}")
        socketio.emit("status", {"state": "ready", "msg": "Ready"})

    voice_engine.set_callback(handle_voice_command)
    voice_engine.start_listening()

    socketio.run(app, host=config.HOST, port=config.PORT,
                 debug=config.DEBUG_MODE, allow_unsafe_werkzeug=True)


if __name__ == "__main__":
    start_server()
