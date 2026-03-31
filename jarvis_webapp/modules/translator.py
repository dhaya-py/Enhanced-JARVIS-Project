"""
JARVIS Translator — uses MyMemory free API
"""
import requests
import re


LANG_MAP = {
    "tamil": "ta", "hindi": "hi", "telugu": "te", "kannada": "kn",
    "malayalam": "ml", "bengali": "bn", "marathi": "mr", "gujarati": "gu",
    "punjabi": "pa", "urdu": "ur", "french": "fr", "spanish": "es",
    "german": "de", "italian": "it", "portuguese": "pt", "russian": "ru",
    "japanese": "ja", "chinese": "zh", "korean": "ko", "arabic": "ar",
    "dutch": "nl", "swedish": "sv", "norwegian": "no", "danish": "da",
    "turkish": "tr", "polish": "pl", "czech": "cs", "greek": "el",
    "hebrew": "he", "thai": "th", "vietnamese": "vi", "indonesian": "id",
    "malay": "ms", "english": "en",
}


class Translator:

    def translate(self, command: str) -> str:
        """Parse and execute a translation command"""
        low = command.lower().strip()
        for w in ["translate", "say", "how to say", "in", "to"]:
            pass  # parse manually

        # Pattern: "translate [text] to [language]"
        m = re.search(r'translate\s+(.+?)\s+to\s+(\w+)', low)
        if m:
            text = m.group(1).strip()
            lang = m.group(2).strip()
            return self._do_translate(text, lang)

        # Pattern: "say [text] in [language]"
        m2 = re.search(r'say\s+(.+?)\s+in\s+(\w+)', low)
        if m2:
            text = m2.group(1).strip()
            lang = m2.group(2).strip()
            return self._do_translate(text, lang)

        # Pattern: "how to say [text] in [language]"
        m3 = re.search(r'how to say\s+(.+?)\s+in\s+(\w+)', low)
        if m3:
            text = m3.group(1).strip()
            lang = m3.group(2).strip()
            return self._do_translate(text, lang)

        return ("I couldn't parse that translation request, sir. "
                "Try: 'translate hello to Tamil' or 'say good morning in French'.")

    def _do_translate(self, text: str, lang_name: str) -> str:
        lang_code = LANG_MAP.get(lang_name.lower())
        if not lang_code:
            supported = ", ".join(sorted(LANG_MAP.keys())[:20])
            return f"I don't recognize '{lang_name}' as a language, sir. Supported: {supported}..."

        try:
            url = "https://api.mymemory.translated.net/get"
            params = {"q": text, "langpair": f"en|{lang_code}"}
            r = requests.get(url, params=params, timeout=8)
            data = r.json()
            translated = data.get("responseData", {}).get("translatedText", "")
            if translated and translated.lower() != text.lower():
                return (f"Translation to {lang_name.title()}, sir:\n\n"
                        f"📝 Original: {text}\n"
                        f"🌍 {lang_name.title()}: {translated}")
            return f"Translation service returned no result for '{text}' → {lang_name}, sir."
        except Exception as e:
            return f"Translation failed, sir. Please check your internet connection. ({e})"

    def get_supported_languages(self) -> str:
        langs = sorted(LANG_MAP.keys())
        return "Supported languages, sir:\n" + ", ".join(l.title() for l in langs)


translator = Translator()
