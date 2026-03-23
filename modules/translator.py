"""
Translator Module
Uses deep-translator (free Google Translate wrapper)
"""

import re

class Translator:
    """Language translation"""

    def __init__(self):
        self.translator = None
        self._init_translator()

    def _init_translator(self):
        """Initialize translator"""
        try:
            from deep_translator import GoogleTranslator
            self.translator = GoogleTranslator
        except ImportError:
            self.translator = None

    def translate(self, command: str) -> str:
        """Parse and translate from natural language command"""
        if not self.translator:
            return "🌍 Translation is not available. Install deep-translator: pip install deep-translator"

        try:
            cmd = command.lower()

            # Pattern: "translate [text] to [language]"
            match = re.search(r'translate\s+(.+?)\s+to\s+(\w+)', cmd)
            if not match:
                # Pattern: "say [text] in [language]"
                match = re.search(r'(?:say|how to say)\s+(.+?)\s+in\s+(\w+)', cmd)

            if match:
                text = match.group(1).strip()
                target_lang = match.group(2).strip()

                # Map common language names to codes
                lang_map = {
                    'spanish': 'es', 'french': 'fr', 'german': 'de',
                    'italian': 'it', 'portuguese': 'pt', 'russian': 'ru',
                    'japanese': 'ja', 'chinese': 'zh-CN', 'korean': 'ko',
                    'arabic': 'ar', 'hindi': 'hi', 'tamil': 'ta',
                    'telugu': 'te', 'bengali': 'bn', 'urdu': 'ur',
                    'dutch': 'nl', 'swedish': 'sv', 'turkish': 'tr',
                    'thai': 'th', 'vietnamese': 'vi', 'polish': 'pl',
                    'indonesian': 'id', 'malay': 'ms', 'filipino': 'tl',
                }

                lang_code = lang_map.get(target_lang, target_lang)

                result = self.translator(source='auto', target=lang_code).translate(text)
                return f"🌍 Translation ({target_lang.title()}):\n\"{text}\" → \"{result}\""

            return "🌍 Please specify: translate [text] to [language]\nExample: translate hello to spanish"

        except Exception as e:
            return f"🌍 Translation error: {e}"

translator = Translator()
