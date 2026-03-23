"""
Jarvis Web Application - Flask + WebSocket Server
Iron Man–inspired AI command center
"""

import sys
import os
import threading
import time
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit

from config.settings import config
from core.database import db
from core.intent_detector import intent_detector

# Import modules
from modules.system_actions import system_actions
from modules.web_actions import web_actions
from modules.information import info_provider
from modules.gpt_integration import gpt

# Import new modules
from modules.ai_chat import ai_chat
from modules.sentiment import sentiment_analyzer
from modules.summarizer import text_summarizer
from modules.knowledge import knowledge_base
from modules.news import news_fetcher
from modules.calculator import smart_calculator
from modules.translator import translator
from modules.notes import notes_manager
from modules.reminders import reminder_manager
from modules.planner import task_planner
from modules.entertainment import entertainment
from modules.security_tools import security_tools
from modules.file_manager import file_manager

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'jarvis-secret-key-2024'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# ── System Stats Background Thread ──────────────────────────────────────
import psutil

def system_stats_thread():
    """Background thread to emit system stats every 2 seconds"""
    while True:
        try:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage('C:' if os.name == 'nt' else '/')
            net = psutil.net_io_counters()
            battery = psutil.sensors_battery()

            stats = {
                'cpu': cpu,
                'ram': mem.percent,
                'ram_used': round(mem.used / (1024**3), 1),
                'ram_total': round(mem.total / (1024**3), 1),
                'disk': disk.percent,
                'disk_used': round(disk.used / (1024**3), 1),
                'disk_total': round(disk.total / (1024**3), 1),
                'net_sent': round(net.bytes_sent / (1024**2), 1),
                'net_recv': round(net.bytes_recv / (1024**2), 1),
                'battery': battery.percent if battery else None,
                'plugged': battery.power_plugged if battery else None,
                'timestamp': datetime.now().strftime('%H:%M:%S')
            }
            socketio.emit('system_stats', stats)
        except Exception as e:
            print(f"Stats error: {e}")
        time.sleep(2)

# ── Routes ──────────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')

@app.route('/api/system/info')
def api_system_info():
    """Get system information"""
    try:
        info = system_actions.get_system_info()
        return jsonify({'success': True, 'data': info})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/notes', methods=['GET', 'POST', 'DELETE'])
def api_notes():
    """Notes API"""
    if request.method == 'GET':
        notes = notes_manager.get_all_notes()
        return jsonify({'success': True, 'data': notes})
    elif request.method == 'POST':
        data = request.json
        result = notes_manager.add_note(data.get('title', ''), data.get('content', ''), data.get('category', 'general'))
        return jsonify({'success': True, 'data': result})
    elif request.method == 'DELETE':
        data = request.json
        result = notes_manager.delete_note(data.get('id'))
        return jsonify({'success': result})

@app.route('/api/reminders', methods=['GET', 'POST', 'DELETE'])
def api_reminders():
    """Reminders API"""
    if request.method == 'GET':
        reminders = reminder_manager.get_all_reminders()
        return jsonify({'success': True, 'data': reminders})
    elif request.method == 'POST':
        data = request.json
        result = reminder_manager.add_reminder(data.get('text', ''), data.get('time', ''))
        return jsonify({'success': True, 'data': result})
    elif request.method == 'DELETE':
        data = request.json
        result = reminder_manager.delete_reminder(data.get('id'))
        return jsonify({'success': result})

@app.route('/api/tasks', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_tasks():
    """Tasks API"""
    if request.method == 'GET':
        tasks = task_planner.get_all_tasks()
        return jsonify({'success': True, 'data': tasks})
    elif request.method == 'POST':
        data = request.json
        result = task_planner.add_task(data.get('title', ''), data.get('priority', 'medium'))
        return jsonify({'success': True, 'data': result})
    elif request.method == 'PUT':
        data = request.json
        result = task_planner.toggle_task(data.get('id'))
        return jsonify({'success': result})
    elif request.method == 'DELETE':
        data = request.json
        result = task_planner.delete_task(data.get('id'))
        return jsonify({'success': result})

@app.route('/api/news')
def api_news():
    """Get news"""
    category = request.args.get('category', 'tech')
    news = news_fetcher.get_news(category)
    return jsonify({'success': True, 'data': news})

@app.route('/api/logs')
def api_logs():
    """Get recent logs"""
    logs = db.get_recent_logs(50)
    return jsonify({'success': True, 'data': [
        {'id': l[0], 'command': l[1], 'response': l[2], 'timestamp': l[3]}
        for l in logs
    ]})

@app.route('/api/stats')
def api_stats():
    """Get database stats"""
    stats = db.get_stats()
    return jsonify({'success': True, 'data': stats})

# ── WebSocket Events ────────────────────────────────────────────────────

@socketio.on('connect')
def handle_connect():
    """Client connected"""
    emit('status', {'message': 'Connected to Jarvis', 'type': 'success'})
    print("✓ Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    """Client disconnected"""
    print("✗ Client disconnected")

@socketio.on('command')
def handle_command(data):
    """Process user command from web UI"""
    command = data.get('text', '').strip()
    if not command:
        return

    emit('status', {'message': 'Processing...', 'type': 'processing'})

    try:
        response = process_command(command)
        emit('response', {
            'text': response,
            'command': command,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })
        # Log interaction
        db.log_interaction(command, response)
    except Exception as e:
        emit('response', {
            'text': f'Error: {str(e)}',
            'command': command,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })

    emit('status', {'message': 'Ready', 'type': 'ready'})

# ── Command Processing ──────────────────────────────────────────────────

def process_command(command: str) -> str:
    """Process a user command and return response"""
    cmd = command.lower().strip()

    # ── Direct keyword matching for new modules ─────────────────────

    # Sentiment analysis
    if cmd.startswith(('analyze sentiment', 'sentiment of', 'how does this feel', 'emotion of')):
        text = cmd.replace('analyze sentiment', '').replace('sentiment of', '').replace('how does this feel', '').replace('emotion of', '').strip()
        if text:
            return sentiment_analyzer.analyze(text)
        return "Please provide text to analyze. Example: 'analyze sentiment I love this project'"

    # Summarize
    if cmd.startswith(('summarize', 'summary of', 'tldr')):
        text = cmd.replace('summarize', '').replace('summary of', '').replace('tldr', '').strip()
        if text:
            return text_summarizer.summarize(text)
        return "Please provide text or URL to summarize."

    # Calculator
    if cmd.startswith(('calculate', 'calc', 'math', 'what is')) and any(c in cmd for c in '+-*/^%'):
        expr = cmd.replace('calculate', '').replace('calc', '').replace('math', '').replace('what is', '').strip()
        return smart_calculator.calculate(expr)

    # Unit conversion
    if ' to ' in cmd and ('convert' in cmd or any(u in cmd for u in ['km', 'miles', 'celsius', 'fahrenheit', 'kg', 'pounds', 'meters', 'feet'])):
        return smart_calculator.convert(cmd)

    # Translation
    if cmd.startswith(('translate', 'say in', 'how to say')):
        return translator.translate(cmd)

    # Knowledge / Wikipedia
    if cmd.startswith(('who is', 'what is', 'tell me about', 'define', 'meaning of', 'wiki')):
        query = cmd.replace('who is', '').replace('what is', '').replace('tell me about', '').replace('define', '').replace('meaning of', '').replace('wiki', '').strip()
        if query:
            return knowledge_base.search(query)

    # News
    if cmd.startswith(('news', 'latest news', 'headlines', 'whats happening')):
        category = 'general'
        for cat in ['tech', 'sports', 'science', 'business', 'world']:
            if cat in cmd:
                category = cat
                break
        return news_fetcher.get_news_text(category)

    # Notes
    if cmd.startswith(('note', 'add note', 'save note', 'write note')):
        text = cmd.replace('add note', '').replace('save note', '').replace('write note', '').replace('note', '').strip()
        if text:
            return notes_manager.add_note_quick(text)
        return "What would you like to note down?"

    if cmd.startswith(('show notes', 'my notes', 'list notes', 'read notes')):
        return notes_manager.get_notes_text()

    # Reminders
    if cmd.startswith(('remind me', 'set reminder', 'reminder')):
        text = cmd.replace('remind me', '').replace('set reminder', '').replace('reminder', '').strip()
        if text:
            return reminder_manager.add_reminder_quick(text)
        return "What would you like to be reminded about?"

    if cmd.startswith(('show reminders', 'my reminders', 'list reminders')):
        return reminder_manager.get_reminders_text()

    # Tasks / Planner
    if cmd.startswith(('add task', 'new task', 'todo')):
        text = cmd.replace('add task', '').replace('new task', '').replace('todo', '').strip()
        if text:
            return task_planner.add_task_quick(text)
        return "What task would you like to add?"

    if cmd.startswith(('show tasks', 'my tasks', 'list tasks', 'to do list', 'todolist')):
        return task_planner.get_tasks_text()

    # Daily briefing
    if cmd.startswith(('briefing', 'daily briefing', 'morning briefing', 'good morning')):
        return generate_briefing()

    # Entertainment
    if cmd.startswith(('joke', 'tell me a joke', 'make me laugh')):
        return entertainment.get_joke()

    if cmd.startswith(('quote', 'motivate me', 'inspiration', 'motivational')):
        return entertainment.get_quote()

    if cmd.startswith(('fun fact', 'interesting fact', 'did you know', 'tell me something')):
        return entertainment.get_fun_fact()

    if cmd.startswith(('trivia', 'quiz', 'game')):
        return entertainment.get_trivia()

    # Password generator
    if cmd.startswith(('generate password', 'password', 'random password')):
        return security_tools.generate_password()

    # File search
    if cmd.startswith(('find file', 'search file', 'locate file')):
        name = cmd.replace('find file', '').replace('search file', '').replace('locate file', '').strip()
        if name:
            return file_manager.search_files(name)
        return "What file are you looking for?"

    # System info
    if cmd in ('system info', 'system status', 'system monitor', 'pc status', 'computer status'):
        return get_system_info_text()

    # ── Fall through to intent detection ────────────────────────────
    intent, action_type, confidence = intent_detector.detect_intent(command)

    if intent and confidence >= config.INTENT_THRESHOLD:
        if action_type == "system":
            return handle_system_action(intent, command)
        elif action_type == "web":
            return handle_web_action(intent, command)
        elif action_type == "info":
            return handle_info_action(intent, command)
        elif action_type == "control":
            return handle_control(intent, command)

    # ── Fall back to AI chat ────────────────────────────────────────
    return ai_chat.get_response(command)


def handle_system_action(intent, command):
    """Handle system actions"""
    action_map = {
        'open_notepad': lambda: system_actions.open_application("notepad"),
        'open_chrome': lambda: system_actions.open_application("chrome"),
        'open_calculator': lambda: system_actions.open_application("calculator"),
        'open_explorer': lambda: system_actions.open_application("explorer"),
        'close_window': lambda: system_actions.close_window(),
        'close_chrome': lambda: system_actions.close_application("chrome"),
        'close_notepad': lambda: system_actions.close_application("notepad"),
        'take_screenshot': lambda: system_actions.take_screenshot(),
        'lock_screen': lambda: system_actions.lock_screen(),
        'shutdown_system': lambda: system_actions.shutdown_system(),
        'restart_system': lambda: system_actions.restart_system(),
        'sleep_system': lambda: system_actions.sleep_system(),
    }
    if intent in action_map:
        success, msg = action_map[intent]()
        return msg
    return f"System action '{intent}' is not yet implemented"

def handle_web_action(intent, command):
    """Handle web actions"""
    site_map = {
        'open_youtube': 'youtube',
        'open_facebook': 'facebook',
        'open_twitter': 'twitter',
        'open_linkedin': 'linkedin',
        'open_github': 'github',
    }
    if intent in site_map:
        success, msg = web_actions.open_website(site_map[intent])
        return msg
    elif intent == 'google_search':
        query = command.replace("search", "").replace("google", "").replace("for", "").strip()
        if query:
            success, msg = web_actions.google_search(query)
            return msg
        return "What would you like me to search for?"
    return f"Web action '{intent}' is not yet implemented"

def handle_info_action(intent, command):
    """Handle info queries"""
    info_map = {
        'get_time': lambda: info_provider.get_time(),
        'get_date': lambda: info_provider.get_date(),
        'about_jarvis': lambda: info_provider.get_about_jarvis(),
        'show_help': lambda: info_provider.get_help(),
        'acknowledge': lambda: info_provider.acknowledge(),
    }
    if intent == 'get_weather':
        city = "London"
        success, msg = info_provider.get_weather(city)
        return msg
    if intent in info_map:
        return info_map[intent]()
    return ai_chat.get_response(command)

def handle_control(intent, command):
    """Handle control commands"""
    if intent == 'stop':
        return "Jarvis is in standby mode."
    elif intent == 'exit':
        return "Goodbye! Jarvis signing off."
    return "Control action not recognized"

def get_system_info_text():
    """Get formatted system info"""
    try:
        info = system_actions.get_system_info()
        return (
            f"🖥️ System Status:\n"
            f"• OS: {info.get('os', 'N/A')} {info.get('os_version', '')}\n"
            f"• CPU: {info.get('cpu_percent', 0)}% ({info.get('cpu_count', 0)} cores)\n"
            f"• RAM: {info.get('memory_percent', 0)}%\n"
            f"• Disk: {info.get('disk_percent', 0)}%"
        )
    except:
        return "Unable to fetch system information."

def generate_briefing():
    """Generate a daily briefing"""
    parts = []
    parts.append("☀️ Good day! Here's your briefing:\n")
    parts.append(f"📅 {info_provider.get_date()}")
    parts.append(f"🕐 {info_provider.get_time()}")

    tasks = task_planner.get_pending_count()
    if tasks > 0:
        parts.append(f"📋 You have {tasks} pending task(s)")

    reminders = reminder_manager.get_active_count()
    if reminders > 0:
        parts.append(f"🔔 You have {reminders} active reminder(s)")

    try:
        news_text = news_fetcher.get_headline()
        if news_text:
            parts.append(f"📰 Top headline: {news_text}")
    except:
        pass

    parts.append(f"\n💡 {entertainment.get_quote_short()}")
    return "\n".join(parts)


# ── Main ────────────────────────────────────────────────────────────────

def run_server():
    """Start the Jarvis web server"""
    print("=" * 60)
    print("  J.A.R.V.I.S. — Web Command Center")
    print("  Open http://localhost:5000 in your browser")
    print("=" * 60)

    # Start system stats background thread
    stats_thread = threading.Thread(target=system_stats_thread, daemon=True)
    stats_thread.start()

    # Start reminder checker
    reminder_thread = threading.Thread(target=reminder_manager.check_reminders_loop, args=(socketio,), daemon=True)
    reminder_thread.start()

    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)

if __name__ == '__main__':
    run_server()
