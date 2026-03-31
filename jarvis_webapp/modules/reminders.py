"""
JARVIS Reminders Manager
"""
import time
from datetime import datetime
from core.database import db


class ReminderManager:

    def add_reminder(self, text: str, remind_at: str = None) -> dict:
        return db.add_reminder(text, remind_at)

    def add_reminder_quick(self, text: str) -> str:
        if not text:
            return "What would you like me to remind you about, sir?"
        db.add_reminder(text)
        return f"Reminder set, sir: '{text}'"

    def get_all_reminders(self) -> list:
        return db.get_all_reminders()

    def get_reminders_text(self) -> str:
        reminders = db.get_all_reminders()
        active = [r for r in reminders if not r['done']]
        if not active:
            return "You have no active reminders, sir."
        lines = [f"Active reminders ({len(active)}), sir:\n"]
        for r in active:
            time_str = f" — {r['remind_at']}" if r.get('remind_at') else ""
            lines.append(f"🔔 {r['text']}{time_str}")
        return "\n".join(lines)

    def mark_done(self, reminder_id: int) -> bool:
        return db.mark_reminder_done(reminder_id)

    def delete_reminder(self, reminder_id: int) -> bool:
        return db.delete_reminder(reminder_id)

    def get_active_count(self) -> int:
        return db.get_active_reminders_count()

    def check_reminders_loop(self, socketio):
        """Background loop to check time-based reminders"""
        while True:
            try:
                reminders = db.get_all_reminders()
                now_str = datetime.now().strftime("%H:%M")
                for r in reminders:
                    if not r['done'] and r.get('remind_at'):
                        if r['remind_at'] == now_str:
                            socketio.emit('reminder_alert', {
                                'id': r['id'],
                                'text': r['text']
                            })
                            db.mark_reminder_done(r['id'])
            except Exception:
                pass
            time.sleep(30)


reminder_manager = ReminderManager()
