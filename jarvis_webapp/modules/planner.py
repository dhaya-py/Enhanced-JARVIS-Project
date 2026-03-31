"""
JARVIS Task Planner — task management with priority
"""
from core.database import db


class TaskPlanner:

    def add_task(self, title: str, priority: str = "medium") -> dict:
        priority = priority.lower()
        if priority not in ("high", "medium", "low"):
            priority = "medium"
        return db.add_task(title, priority)

    def add_task_quick(self, text: str) -> str:
        if not text:
            return "What task would you like to add, sir?"
        priority = "medium"
        if "urgent" in text.lower() or "asap" in text.lower() or "important" in text.lower():
            priority = "high"
        elif "later" in text.lower() or "sometime" in text.lower():
            priority = "low"
        clean = text.lower().replace("urgent", "").replace("asap", "").replace("important", "").strip()
        db.add_task(text, priority)
        return f"Task added with {priority} priority: '{text}', sir."

    def get_all_tasks(self) -> list:
        return db.get_all_tasks()

    def get_tasks_text(self) -> str:
        tasks = db.get_all_tasks()
        if not tasks:
            return "Your task list is empty, sir. A clean slate awaits."
        pending = [t for t in tasks if not t['done']]
        done = [t for t in tasks if t['done']]
        lines = [f"Task overview — {len(pending)} pending, {len(done)} completed:\n"]
        priority_icons = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        for t in pending[:8]:
            icon = priority_icons.get(t['priority'], "⚪")
            lines.append(f"{icon} {t['title']} [{t['priority'].upper()}]")
        if len(pending) > 8:
            lines.append(f"...and {len(pending) - 8} more tasks.")
        if done:
            lines.append(f"\n✅ Completed: {len(done)} task(s)")
        return "\n".join(lines)

    def toggle_task(self, task_id: int) -> bool:
        return db.toggle_task(task_id)

    def delete_task(self, task_id: int) -> bool:
        return db.delete_task(task_id)

    def get_pending_count(self) -> int:
        return db.get_pending_tasks_count()


task_planner = TaskPlanner()
