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
from modules.clipboard_manager import clipboard_manager
from modules.process_manager import process_manager
from modules.web_scraper import web_scraper

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

@app.route('/api/processes')
def api_processes():
    """Get running processes"""
    summary = process_manager.get_summary()
    return jsonify({'success': True, 'data': summary})

@app.route('/api/clipboard')
def api_clipboard():
    """Get clipboard history"""
    history = clipboard_manager.get_history_list()
    return jsonify({'success': True, 'data': history})

@app.route('/api/weather')
def api_weather():
    """Get weather info"""
    city = request.args.get('city', 'London')
    try:
        import requests as req
        response = req.get(f'https://wttr.in/{city}?format=j1', timeout=5)
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            return jsonify({'success': True, 'data': {
                'temp': current.get('temp_C', '--'),
                'feels_like': current.get('FeelsLikeC', '--'),
                'humidity': current.get('humidity', '--'),
                'desc': current.get('weatherDesc', [{}])[0].get('value', 'Unknown'),
                'wind': current.get('windspeedKmph', '--'),
                'city': city
            }})
    except:
        pass
    return jsonify({'success': False, 'data': None})

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

    # Process management
    if cmd.startswith(('show processes', 'running processes', 'list processes', 'active processes', 'what is running')):
        return process_manager.list_processes()

    if cmd.startswith(('kill process', 'end process', 'terminate process', 'stop process')):
        name = cmd.replace('kill process', '').replace('end process', '').replace('terminate process', '').replace('stop process', '').strip()
        if name:
            return process_manager.kill_process(name)
        return "Which process should I terminate? Give me a name or PID."

    # Clipboard
    if cmd.startswith(('clipboard', 'show clipboard', 'clipboard history', 'what did i copy')):
        return clipboard_manager.get_history()

    # Web scraper
    if cmd.startswith(('scrape', 'extract text from', 'read webpage')):
        url = cmd.replace('scrape', '').replace('extract text from', '').replace('read webpage', '').strip()
        if url:
            return web_scraper.scrape_text(url)
        return "Please provide a URL to scrape. Example: scrape example.com"

    # Disk usage
    if cmd in ('disk space', 'storage space', 'disk usage', 'check storage', 'how much space'):
        return file_manager.get_disk_usage()

    # IP address
    if cmd in ('ip address', 'my ip', 'what is my ip'):
        try:
            import requests as req
            ip = req.get('https://api.ipify.org', timeout=5).text
            return f"🌐 Your public IP address: **{ip}**"
        except:
            return "❌ Could not fetch your IP address. Check internet connection."

    # System info
    if cmd in ('system info', 'system status', 'system monitor', 'pc status', 'computer status', 'check system', 'how is my pc'):
        return get_system_info_text()

    # Clear chat
    if cmd in ('clear chat', 'clear screen', 'reset chat'):
        return '__CLEAR_CHAT__'

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
        elif action_type == "entertainment":
            return handle_entertainment(intent, command)
        elif action_type == "productivity":
            return handle_productivity(intent, command)
        elif action_type == "ai":
            return handle_ai_action(intent, command)
        elif action_type == "tools":
            return handle_tools_action(intent, command)

    # ── Fall back: fuzzy suggestions or AI chat ───────────────────
    suggestions = intent_detector.get_fuzzy_suggestions(command)
    if suggestions:
        return suggestions
    return ai_chat.get_response(command)


def handle_system_action(intent, command):
    """Handle system actions"""
    action_map = {
        'open_notepad': lambda: system_actions.open_application("notepad"),
        'open_chrome': lambda: system_actions.open_application("chrome"),
        'open_calculator': lambda: system_actions.open_application("calculator"),
        'open_explorer': lambda: system_actions.open_application("explorer"),
        'open_cmd': lambda: system_actions.open_application("cmd"),
        'open_powershell': lambda: system_actions.open_application("powershell"),
        'open_paint': lambda: system_actions.open_application("paint"),
        'open_taskmgr': lambda: system_actions.open_application("taskmgr"),
        'open_settings': lambda: system_actions.open_application("settings"),
        'open_control_panel': lambda: system_actions.open_application("control panel"),
        'open_vscode': lambda: system_actions.open_application("vscode"),
        'open_word': lambda: system_actions.open_application("word"),
        'open_excel': lambda: system_actions.open_application("excel"),
        'open_powerpoint': lambda: system_actions.open_application("powerpoint"),
        'open_spotify': lambda: system_actions.open_application("spotify"),
        'open_discord': lambda: system_actions.open_application("discord"),
        'open_telegram': lambda: system_actions.open_application("telegram"),
        'open_whatsapp': lambda: system_actions.open_application("whatsapp"),
        'open_vlc': lambda: system_actions.open_application("vlc"),
        'open_zoom': lambda: system_actions.open_application("zoom"),
        'open_teams': lambda: system_actions.open_application("teams"),
        'open_onenote': lambda: system_actions.open_application("onenote"),
        'open_outlook': lambda: system_actions.open_application("outlook"),
        'open_slack': lambda: system_actions.open_application("slack"),
        'open_obs': lambda: system_actions.open_application("obs"),
        'open_brave': lambda: system_actions.open_application("brave"),
        'open_firefox': lambda: system_actions.open_application("firefox"),
        'open_edge': lambda: system_actions.open_application("edge"),
        'open_snipping_tool': lambda: system_actions.open_application("snipping tool"),
        'close_window': lambda: system_actions.close_window(),
        'close_chrome': lambda: system_actions.close_application("chrome"),
        'close_notepad': lambda: system_actions.close_application("notepad"),
        'close_vlc': lambda: system_actions.close_application("vlc"),
        'close_zoom': lambda: system_actions.close_application("zoom"),
        'close_teams': lambda: system_actions.close_application("teams"),
        'close_firefox': lambda: system_actions.close_application("firefox"),
        'close_edge': lambda: system_actions.close_application("edge"),
        'close_brave': lambda: system_actions.close_application("brave"),
        'close_slack': lambda: system_actions.close_application("slack"),
        'close_all': lambda: (True, "Close all is disabled for safety."),
        'take_screenshot': lambda: system_actions.take_screenshot(),
        'lock_screen': lambda: system_actions.lock_screen(),
        'shutdown_system': lambda: system_actions.shutdown_system(),
        'restart_system': lambda: system_actions.restart_system(),
        'sleep_system': lambda: system_actions.sleep_system(),
        'system_info': lambda: (True, get_system_info_text()),
        'list_processes': lambda: (True, process_manager.list_processes()),
        'disk_usage': lambda: (True, file_manager.get_disk_usage()),
        'battery_status': lambda: (True, get_battery_text()),
    }
    if intent == 'kill_process':
        name = command.lower().replace('kill process', '').replace('end process', '').replace('stop process', '').replace('terminate process', '').strip()
        if name:
            return process_manager.kill_process(name)
        return "Which process should I terminate?"
    if intent in action_map:
        result = action_map[intent]()
        if isinstance(result, tuple):
            success, msg = result
            return msg
        return str(result)
    return f"System action '{intent}' is not yet implemented"

def handle_web_action(intent, command):
    """Handle web actions"""
    site_map = {
        'open_youtube': 'youtube',
        'open_facebook': 'facebook',
        'open_twitter': 'twitter',
        'open_linkedin': 'linkedin',
        'open_github': 'github',
        'open_instagram': 'instagram',
        'open_reddit': 'reddit',
        'open_gmail': 'gmail',
        'open_amazon': 'amazon',
        'open_netflix': 'netflix',
        'open_stackoverflow': 'stackoverflow',
        'open_chatgpt': 'chatgpt',
        'open_whatsapp_web': 'whatsapp',
        'open_wikipedia': 'wikipedia',
        'open_pinterest': 'pinterest',
        'open_twitch': 'twitch',
        'open_spotify_web': 'spotify',
        'open_medium': 'medium',
        'open_w3schools': 'w3schools',
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
        'greeting': lambda: ai_chat.get_response(command),
        'daily_briefing': lambda: generate_briefing(),
    }
    if intent == 'get_weather':
        city = "London"
        success, msg = info_provider.get_weather(city)
        return msg
    if intent in ('get_news', 'get_tech_news', 'get_sports_news', 'get_world_news', 'get_science_news', 'get_business_news'):
        cat_map = {'get_news': 'general', 'get_tech_news': 'tech', 'get_sports_news': 'sports', 'get_world_news': 'world', 'get_science_news': 'science', 'get_business_news': 'business'}
        return news_fetcher.get_news_text(cat_map.get(intent, 'general'))
    if intent == 'get_ip':
        try:
            import requests as req
            ip = req.get('https://api.ipify.org', timeout=5).text
            return f"🌐 Your public IP address: **{ip}**"
        except:
            return "❌ Could not fetch IP address."
    if intent in info_map:
        return info_map[intent]()
    return ai_chat.get_response(command)

def handle_entertainment(intent, command):
    """Handle entertainment-related intents"""
    ent_map = {
        'tell_joke': lambda: entertainment.get_joke(),
        'get_quote': lambda: entertainment.get_quote(),
        'get_fun_fact': lambda: entertainment.get_fun_fact(),
        'trivia_game': lambda: entertainment.get_trivia(),
    }
    if intent in ent_map:
        return ent_map[intent]()
    return entertainment.get_joke()

def handle_productivity(intent, command):
    """Handle productivity-related intents"""
    if intent == 'add_note':
        text = command.lower()
        for prefix in ['add note', 'save note', 'write note', 'note this', 'take a note', 'remember this', 'jot this down']:
            text = text.replace(prefix, '')
        text = text.strip()
        if text:
            return notes_manager.add_note_quick(text)
        return "What would you like to note down?"
    if intent == 'show_notes':
        return notes_manager.get_notes_text()
    if intent == 'set_reminder':
        text = command.lower()
        for prefix in ['remind me', 'set reminder', 'set alarm', 'reminder', "don't let me forget"]:
            text = text.replace(prefix, '')
        text = text.strip()
        if text:
            return reminder_manager.add_reminder_quick(text)
        return "What would you like to be reminded about?"
    if intent == 'show_reminders':
        return reminder_manager.get_reminders_text()
    if intent == 'add_task':
        text = command.lower()
        for prefix in ['add task', 'new task', 'add todo', 'to do', 'create task']:
            text = text.replace(prefix, '')
        text = text.strip()
        if text:
            return task_planner.add_task_quick(text)
        return "What task would you like to add?"
    if intent == 'show_tasks':
        return task_planner.get_tasks_text()
    return "Productivity action not recognized."

def handle_ai_action(intent, command):
    """Handle AI/intelligence intents"""
    if intent == 'analyze_sentiment':
        text = command.lower()
        for prefix in ['analyze sentiment', 'sentiment of', 'how does this sound', 'sentiment analysis']:
            text = text.replace(prefix, '')
        text = text.strip()
        if text:
            return sentiment_analyzer.analyze(text)
        return "Please provide text to analyze."
    if intent == 'calculate':
        expr = command.lower()
        for prefix in ['calculate', 'calc', 'what is', 'do the math', 'compute']:
            expr = expr.replace(prefix, '')
        return smart_calculator.calculate(expr.strip())
    if intent == 'unit_convert':
        return smart_calculator.convert(command)
    if intent == 'translate':
        return translator.translate(command)
    if intent == 'summarize':
        text = command.lower()
        for prefix in ['summarize', 'summary of', 'give me a summary', 'tldr']:
            text = text.replace(prefix, '')
        text = text.strip()
        if text:
            return text_summarizer.summarize(text)
        return "Please provide text to summarize."
    if intent == 'knowledge_search':
        query = command.lower()
        for prefix in ['who is', 'what is a', 'what is', 'tell me about', 'define', 'meaning of', 'wikipedia', 'knowledge']:
            query = query.replace(prefix, '')
        query = query.strip()
        if query:
            return knowledge_base.search(query)
    return ai_chat.get_response(command)

def handle_tools_action(intent, command):
    """Handle tools-related intents"""
    if intent == 'gen_password':
        return security_tools.generate_password()
    if intent == 'search_file':
        name = command.lower()
        for prefix in ['find file', 'search file', 'locate file', 'where is file']:
            name = name.replace(prefix, '')
        name = name.strip()
        if name:
            return file_manager.search_files(name)
        return "What file are you looking for?"
    if intent == 'clipboard_show':
        return clipboard_manager.get_history()
    if intent == 'clipboard_copy':
        text = command.replace('copy to clipboard', '').strip()
        if text:
            return clipboard_manager.copy(text)
        return "What would you like to copy?"
    if intent == 'web_scrape':
        url = command.lower()
        for prefix in ['scrape website', 'extract text from', 'get text from website', 'read webpage', 'scrape']:
            url = url.replace(prefix, '')
        url = url.strip()
        if url:
            return web_scraper.scrape_text(url)
        return "Please provide a URL to scrape."
    return "Tool action not recognized."

def handle_control(intent, command):
    """Handle control commands"""
    if intent == 'stop':
        return "Jarvis is in standby mode."
    elif intent == 'exit':
        return "Goodbye! Jarvis signing off. 👋"
    elif intent == 'clear_chat':
        return '__CLEAR_CHAT__'
    return "Control action not recognized"

def get_battery_text():
    """Get battery status text"""
    try:
        battery = psutil.sensors_battery()
        if battery:
            plug = '⚡ Plugged in' if battery.power_plugged else '🔋 On battery'
            return f"🔋 Battery: {battery.percent}% | {plug}"
        return "🔋 No battery detected (desktop PC)"
    except:
        return "Unable to get battery info"

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
