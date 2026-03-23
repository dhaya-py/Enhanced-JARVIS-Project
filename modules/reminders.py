"""
Reminders Module
Time-based reminder system with SQLite storage
"""

import sqlite3
import time
from datetime import datetime, timedelta
from config.settings import config

class ReminderManager:
    """Manage reminders with scheduling"""

    def __init__(self):
        self.db_path = config.DB_PATH
        self._init_table()

    def _init_table(self):
        """Create reminders table"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS reminders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        text TEXT NOT NULL,
                        remind_at TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        is_active INTEGER DEFAULT 1,
                        is_notified INTEGER DEFAULT 0
                    )
                """)
        except Exception as e:
            print(f"Reminders table error: {e}")

    def add_reminder(self, text: str, remind_time: str) -> dict:
        """Add a reminder"""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "INSERT INTO reminders (text, remind_at, created_at) VALUES (?, ?, ?)",
                    (text, remind_time, now)
                )
                return {'id': cursor.lastrowid, 'text': text, 'remind_at': remind_time}
        except Exception as e:
            return {'error': str(e)}

    def add_reminder_quick(self, text: str) -> str:
        """Quick add reminder from natural language"""
        # Parse simple time expressions
        now = datetime.now()

        if 'in' in text:
            # "in 5 minutes", "in 1 hour"
            import re
            match = re.search(r'in\s+(\d+)\s*(minute|min|hour|hr|second|sec)', text)
            if match:
                amount = int(match.group(1))
                unit = match.group(2).lower()
                reminder_text = text.split('in')[0].strip() or text

                if unit.startswith('min'):
                    remind_at = now + timedelta(minutes=amount)
                elif unit.startswith('hr') or unit.startswith('hour'):
                    remind_at = now + timedelta(hours=amount)
                else:
                    remind_at = now + timedelta(seconds=amount)

                result = self.add_reminder(reminder_text, remind_at.strftime('%Y-%m-%d %H:%M:%S'))
                return f"🔔 Reminder set for {remind_at.strftime('%I:%M %p')}: \"{reminder_text}\""

        # Default: remind in 30 minutes
        remind_at = now + timedelta(minutes=30)
        result = self.add_reminder(text, remind_at.strftime('%Y-%m-%d %H:%M:%S'))
        return f"🔔 Reminder set for {remind_at.strftime('%I:%M %p')}: \"{text}\""

    def get_all_reminders(self) -> list:
        """Get all active reminders"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT id, text, remind_at, created_at, is_active FROM reminders WHERE is_active = 1 ORDER BY remind_at ASC"
                )
                return [{'id': r[0], 'text': r[1], 'remind_at': r[2], 'created_at': r[3], 'is_active': r[4]} for r in cursor.fetchall()]
        except:
            return []

    def get_reminders_text(self) -> str:
        """Get reminders as formatted text"""
        reminders = self.get_all_reminders()
        if not reminders:
            return "🔔 No active reminders. Say 'remind me [text] in [time]' to set one."

        text = f"🔔 Active Reminders ({len(reminders)}):\n\n"
        for r in reminders:
            text += f"• {r['text']}\n  ⏰ {r['remind_at']}\n\n"
        return text

    def get_active_count(self) -> int:
        """Get count of active reminders"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM reminders WHERE is_active = 1")
                return cursor.fetchone()[0]
        except:
            return 0

    def delete_reminder(self, reminder_id: int) -> bool:
        """Delete a reminder"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
                return True
        except:
            return False

    def check_reminders_loop(self, socketio=None):
        """Background loop to check for due reminders"""
        while True:
            try:
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.execute(
                        "SELECT id, text FROM reminders WHERE remind_at <= ? AND is_active = 1 AND is_notified = 0",
                        (now,)
                    )
                    due = cursor.fetchall()

                    for reminder_id, text in due:
                        # Mark as notified
                        conn.execute("UPDATE reminders SET is_notified = 1, is_active = 0 WHERE id = ?", (reminder_id,))

                        # Emit notification via WebSocket
                        if socketio:
                            socketio.emit('notification', {
                                'type': 'reminder',
                                'title': '🔔 Reminder',
                                'text': text,
                                'timestamp': now
                            })
            except:
                pass
            time.sleep(30)  # Check every 30 seconds

reminder_manager = ReminderManager()
