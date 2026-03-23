"""
Notes Manager Module
SQLite-backed note-taking system
"""

import sqlite3
from datetime import datetime
from config.settings import config

class NotesManager:
    """Manage notes with SQLite storage"""

    def __init__(self):
        self.db_path = config.DB_PATH
        self._init_table()

    def _init_table(self):
        """Create notes table"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS notes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        category TEXT DEFAULT 'general',
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    )
                """)
        except Exception as e:
            print(f"Notes table error: {e}")

    def add_note(self, title: str, content: str, category: str = 'general') -> dict:
        """Add a note"""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "INSERT INTO notes (title, content, category, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                    (title, content, category, now, now)
                )
                return {'id': cursor.lastrowid, 'title': title, 'content': content, 'category': category}
        except Exception as e:
            return {'error': str(e)}

    def add_note_quick(self, text: str) -> str:
        """Quick add note from voice/text command"""
        title = text[:50] + ('...' if len(text) > 50 else '')
        result = self.add_note(title, text)
        if 'error' in result:
            return f"❌ Error saving note: {result['error']}"
        return f"📝 Note saved: \"{title}\""

    def get_all_notes(self) -> list:
        """Get all notes"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT id, title, content, category, created_at FROM notes ORDER BY id DESC")
                return [{'id': r[0], 'title': r[1], 'content': r[2], 'category': r[3], 'created_at': r[4]} for r in cursor.fetchall()]
        except:
            return []

    def get_notes_text(self) -> str:
        """Get notes as formatted text"""
        notes = self.get_all_notes()
        if not notes:
            return "📝 No notes yet. Say 'add note [text]' to create one."

        text = f"📝 Your Notes ({len(notes)} total):\n\n"
        for note in notes[:10]:
            text += f"• [{note['category']}] {note['title']}\n"
            text += f"  Created: {note['created_at']}\n\n"
        return text

    def delete_note(self, note_id: int) -> bool:
        """Delete a note"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
                return True
        except:
            return False

    def search_notes(self, query: str) -> list:
        """Search notes"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT id, title, content, category, created_at FROM notes WHERE title LIKE ? OR content LIKE ? ORDER BY id DESC",
                    (f'%{query}%', f'%{query}%')
                )
                return [{'id': r[0], 'title': r[1], 'content': r[2], 'category': r[3], 'created_at': r[4]} for r in cursor.fetchall()]
        except:
            return []

notes_manager = NotesManager()
