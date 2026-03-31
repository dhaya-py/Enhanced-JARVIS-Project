"""
JARVIS Database Manager — SQLite persistence layer
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from config.settings import config


class DatabaseManager:
    def __init__(self):
        self.db_path = config.DATABASE_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_conn(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    command TEXT NOT NULL,
                    response TEXT NOT NULL,
                    intent TEXT,
                    action_type TEXT,
                    timestamp TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    category TEXT DEFAULT 'general',
                    pinned INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    priority TEXT DEFAULT 'medium',
                    done INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    completed_at TEXT
                );

                CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    remind_at TEXT,
                    done INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
            """)

    # ── Logs ─────────────────────────────────────────────────────────

    def log_interaction(self, command, response, intent=None, action_type=None):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._get_conn() as conn:
            conn.execute(
                "INSERT INTO logs (command, response, intent, action_type, timestamp) VALUES (?,?,?,?,?)",
                (command, response, intent, action_type, ts)
            )

    def get_recent_logs(self, limit=50):
        with self._get_conn() as conn:
            rows = conn.execute(
                "SELECT * FROM logs ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
        return [dict(r) for r in rows]

    def clear_logs(self):
        with self._get_conn() as conn:
            conn.execute("DELETE FROM logs")

    def get_stats(self):
        with self._get_conn() as conn:
            total = conn.execute("SELECT COUNT(*) FROM logs").fetchone()[0]
            today = conn.execute(
                "SELECT COUNT(*) FROM logs WHERE timestamp LIKE ?",
                (datetime.now().strftime("%Y-%m-%d") + "%",)
            ).fetchone()[0]
            notes_count = conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
            tasks_count = conn.execute("SELECT COUNT(*) FROM tasks WHERE done=0").fetchone()[0]
            reminders_count = conn.execute("SELECT COUNT(*) FROM reminders WHERE done=0").fetchone()[0]
        return {
            "total_commands": total,
            "today_commands": today,
            "notes": notes_count,
            "pending_tasks": tasks_count,
            "active_reminders": reminders_count
        }

    # ── Notes ─────────────────────────────────────────────────────────

    def get_all_notes(self):
        with self._get_conn() as conn:
            rows = conn.execute("SELECT * FROM notes ORDER BY pinned DESC, updated_at DESC").fetchall()
        return [dict(r) for r in rows]

    def add_note(self, title, content, category="general"):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._get_conn() as conn:
            cur = conn.execute(
                "INSERT INTO notes (title, content, category, created_at, updated_at) VALUES (?,?,?,?,?)",
                (title, content, category, now, now)
            )
            return {"id": cur.lastrowid, "title": title, "content": content,
                    "category": category, "created_at": now}

    def update_note(self, note_id, title=None, content=None):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._get_conn() as conn:
            if title and content:
                conn.execute("UPDATE notes SET title=?, content=?, updated_at=? WHERE id=?",
                             (title, content, now, note_id))
            elif content:
                conn.execute("UPDATE notes SET content=?, updated_at=? WHERE id=?",
                             (content, now, note_id))

    def delete_note(self, note_id):
        with self._get_conn() as conn:
            conn.execute("DELETE FROM notes WHERE id=?", (note_id,))
        return True

    # ── Tasks ─────────────────────────────────────────────────────────

    def get_all_tasks(self):
        with self._get_conn() as conn:
            rows = conn.execute(
                "SELECT * FROM tasks ORDER BY done ASC, CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END, created_at DESC"
            ).fetchall()
        return [dict(r) for r in rows]

    def add_task(self, title, priority="medium"):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._get_conn() as conn:
            cur = conn.execute(
                "INSERT INTO tasks (title, priority, created_at) VALUES (?,?,?)",
                (title, priority, now)
            )
            return {"id": cur.lastrowid, "title": title, "priority": priority, "done": 0}

    def toggle_task(self, task_id):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._get_conn() as conn:
            task = conn.execute("SELECT done FROM tasks WHERE id=?", (task_id,)).fetchone()
            if task:
                new_done = 0 if task["done"] else 1
                conn.execute("UPDATE tasks SET done=?, completed_at=? WHERE id=?",
                             (new_done, now if new_done else None, task_id))
        return True

    def delete_task(self, task_id):
        with self._get_conn() as conn:
            conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        return True

    def get_pending_tasks_count(self):
        with self._get_conn() as conn:
            return conn.execute("SELECT COUNT(*) FROM tasks WHERE done=0").fetchone()[0]

    # ── Reminders ─────────────────────────────────────────────────────

    def get_all_reminders(self):
        with self._get_conn() as conn:
            rows = conn.execute("SELECT * FROM reminders ORDER BY done ASC, created_at DESC").fetchall()
        return [dict(r) for r in rows]

    def add_reminder(self, text, remind_at=None):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._get_conn() as conn:
            cur = conn.execute(
                "INSERT INTO reminders (text, remind_at, created_at) VALUES (?,?,?)",
                (text, remind_at, now)
            )
            return {"id": cur.lastrowid, "text": text, "remind_at": remind_at, "done": 0}

    def mark_reminder_done(self, reminder_id):
        with self._get_conn() as conn:
            conn.execute("UPDATE reminders SET done=1 WHERE id=?", (reminder_id,))
        return True

    def delete_reminder(self, reminder_id):
        with self._get_conn() as conn:
            conn.execute("DELETE FROM reminders WHERE id=?", (reminder_id,))
        return True

    def get_active_reminders_count(self):
        with self._get_conn() as conn:
            return conn.execute("SELECT COUNT(*) FROM reminders WHERE done=0").fetchone()[0]

    # ── Settings ─────────────────────────────────────────────────────

    def get_setting(self, key, default=None):
        with self._get_conn() as conn:
            row = conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        return row["value"] if row else default

    def set_setting(self, key, value):
        with self._get_conn() as conn:
            conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?,?)", (key, str(value)))


db = DatabaseManager()
