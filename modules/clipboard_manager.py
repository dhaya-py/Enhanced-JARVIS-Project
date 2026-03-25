"""
Clipboard Manager Module
Track clipboard history and manage copied items
"""

import pyperclip
from datetime import datetime

class ClipboardManager:
    """Clipboard history and management"""

    def __init__(self):
        self.history = []
        self.max_history = 50
        self._last_content = ""

    def copy(self, text: str) -> str:
        """Copy text to clipboard"""
        try:
            pyperclip.copy(text)
            self._add_to_history(text)
            return f"📋 Copied to clipboard: \"{text[:60]}{'...' if len(text) > 60 else ''}\""
        except Exception as e:
            return f"❌ Clipboard error: {e}"

    def paste(self) -> str:
        """Get current clipboard content"""
        try:
            content = pyperclip.paste()
            if content:
                return f"📋 Clipboard content:\n{content[:500]}{'...' if len(content) > 500 else ''}"
            return "📋 Clipboard is empty"
        except Exception as e:
            return f"❌ Clipboard error: {e}"

    def get_history(self) -> str:
        """Get clipboard history"""
        if not self.history:
            return "📋 No clipboard history yet."

        text = f"📋 Clipboard History ({len(self.history)} items):\n\n"
        for i, item in enumerate(self.history[:15], 1):
            content = item['text'][:60] + ('...' if len(item['text']) > 60 else '')
            text += f"  {i}. {content}\n     ⏰ {item['time']}\n\n"
        return text

    def get_history_list(self) -> list:
        """Get history as list"""
        return self.history[:15]

    def clear_history(self) -> str:
        """Clear clipboard history"""
        self.history.clear()
        return "📋 Clipboard history cleared."

    def check_new(self) -> str:
        """Check if clipboard has new content"""
        try:
            current = pyperclip.paste()
            if current and current != self._last_content:
                self._last_content = current
                self._add_to_history(current)
                return current
        except:
            pass
        return None

    def _add_to_history(self, text: str):
        """Add to history"""
        # Don't add duplicates of the last item
        if self.history and self.history[0]['text'] == text:
            return
        self.history.insert(0, {
            'text': text,
            'time': datetime.now().strftime('%H:%M:%S')
        })
        if len(self.history) > self.max_history:
            self.history.pop()

clipboard_manager = ClipboardManager()
