"""
JARVIS Notes Manager — CRUD for notes via database
"""
from core.database import db
from datetime import datetime


class NotesManager:

    def add_note(self, title: str, content: str, category: str = "general") -> dict:
        return db.add_note(title, content, category)

    def add_note_quick(self, text: str) -> str:
        """Add a note from a voice/text command quickly"""
        if not text:
            return "What would you like me to note down, sir?"
        # Auto-title from first words
        words = text.split()
        title = " ".join(words[:4]) if len(words) > 4 else text
        db.add_note(title, text)
        return f"Noted, sir. I've saved: '{text}'"

    def get_all_notes(self) -> list:
        return db.get_all_notes()

    def get_notes_text(self) -> str:
        notes = db.get_all_notes()
        if not notes:
            return "You have no saved notes, sir."
        lines = [f"Your notes ({len(notes)} total), sir:\n"]
        for n in notes[:10]:
            lines.append(f"📝 [{n['category'].upper()}] {n['title']}\n   {n['content'][:80]}...")
        if len(notes) > 10:
            lines.append(f"\n...and {len(notes) - 10} more. Check the Notes panel for full list.")
        return "\n".join(lines)

    def delete_note(self, note_id: int) -> bool:
        return db.delete_note(note_id)

    def update_note(self, note_id: int, title: str = None, content: str = None) -> bool:
        db.update_note(note_id, title, content)
        return True

    def search_notes(self, query: str) -> str:
        notes = db.get_all_notes()
        q = query.lower()
        matches = [n for n in notes if q in n['title'].lower() or q in n['content'].lower()]
        if not matches:
            return f"No notes found matching '{query}', sir."
        lines = [f"Found {len(matches)} note(s) matching '{query}':"]
        for n in matches:
            lines.append(f"• {n['title']}: {n['content'][:60]}...")
        return "\n".join(lines)


notes_manager = NotesManager()
