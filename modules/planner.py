"""
Task Planner Module
To-do list and task management with priorities
"""

import sqlite3
from datetime import datetime
from config.settings import config

class TaskPlanner:
    """Task management system"""

    def __init__(self):
        self.db_path = config.DB_PATH
        self._init_table()

    def _init_table(self):
        """Create tasks table"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        priority TEXT DEFAULT 'medium',
                        is_completed INTEGER DEFAULT 0,
                        created_at TEXT NOT NULL,
                        completed_at TEXT
                    )
                """)
        except Exception as e:
            print(f"Tasks table error: {e}")

    def add_task(self, title: str, priority: str = 'medium') -> dict:
        """Add a task"""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "INSERT INTO tasks (title, priority, created_at) VALUES (?, ?, ?)",
                    (title, priority, now)
                )
                return {'id': cursor.lastrowid, 'title': title, 'priority': priority}
        except Exception as e:
            return {'error': str(e)}

    def add_task_quick(self, text: str) -> str:
        """Quick add task from command"""
        priority = 'medium'
        if 'urgent' in text.lower() or 'high' in text.lower():
            priority = 'high'
            text = text.replace('urgent', '').replace('high priority', '').strip()
        elif 'low' in text.lower():
            priority = 'low'
            text = text.replace('low priority', '').strip()

        result = self.add_task(text, priority)
        emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(priority, '🟡')
        return f"✅ Task added: \"{text}\" {emoji} {priority.title()} priority"

    def get_all_tasks(self) -> list:
        """Get all tasks"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT id, title, priority, is_completed, created_at, completed_at FROM tasks ORDER BY is_completed ASC, CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 WHEN 'low' THEN 3 END, id DESC"
                )
                return [{'id': r[0], 'title': r[1], 'priority': r[2], 'is_completed': r[3], 'created_at': r[4], 'completed_at': r[5]} for r in cursor.fetchall()]
        except:
            return []

    def get_tasks_text(self) -> str:
        """Get tasks as formatted text"""
        tasks = self.get_all_tasks()
        if not tasks:
            return "📋 No tasks yet. Say 'add task [description]' to create one."

        pending = [t for t in tasks if not t['is_completed']]
        completed = [t for t in tasks if t['is_completed']]

        text = f"📋 Tasks ({len(pending)} pending, {len(completed)} done):\n\n"

        if pending:
            text += "📌 Pending:\n"
            for t in pending:
                emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(t['priority'], '🟡')
                text += f"  {emoji} {t['title']}\n"

        if completed:
            text += "\n✅ Completed:\n"
            for t in completed[:5]:
                text += f"  ✓ {t['title']}\n"

        return text

    def toggle_task(self, task_id: int) -> bool:
        """Toggle task completion"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT is_completed FROM tasks WHERE id = ?", (task_id,))
                row = cursor.fetchone()
                if row:
                    new_status = 0 if row[0] else 1
                    completed_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S') if new_status else None
                    conn.execute(
                        "UPDATE tasks SET is_completed = ?, completed_at = ? WHERE id = ?",
                        (new_status, completed_at, task_id)
                    )
                    return True
        except:
            pass
        return False

    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
                return True
        except:
            return False

    def get_pending_count(self) -> int:
        """Get count of pending tasks"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM tasks WHERE is_completed = 0")
                return cursor.fetchone()[0]
        except:
            return 0

task_planner = TaskPlanner()
