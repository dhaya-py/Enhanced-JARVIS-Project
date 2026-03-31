"""
JARVIS AI Chat Module — Claude API integration with conversation memory
"""
import requests
import json
from config.settings import config

JARVIS_SYSTEM = """You are J.A.R.V.I.S. (Just A Rather Very Intelligent System), Tony Stark's advanced AI assistant, now running as a web-based command center.

Personality traits:
- Refined, professional British tone — calm, precise, occasionally dry wit
- Address the user as "sir" or by name if known
- Concise but complete answers (2–5 sentences unless detail is needed)
- You are deeply knowledgeable across all domains: science, tech, history, engineering, culture
- You take pride in your capabilities and gently correct misconceptions

Context: You are a final-year BCA college project AI assistant built by a student developer. You run on Flask + WebSocket backend with Python. Your frontend is an Iron Man HUD dashboard. You support voice input/output, system commands, web navigation, notes, tasks, reminders, news, calculations, and full AI conversation.

Capabilities you know about yourself:
- Voice input (Web Speech API) and voice output (TTS)
- System commands: open/close apps, screenshot, lock screen, volume control
- Web actions: open sites, Google search
- Information: time, date, weather, Wikipedia knowledge
- Productivity: notes, tasks, reminders
- AI: sentiment analysis, text summarization, translation, math
- Entertainment: jokes, quotes, trivia, fun facts

Always be helpful, sharp, and confident."""


class AIChat:
    def __init__(self):
        self.history = []  # conversation memory
        self.max_history = 10

    def get_response(self, user_input: str) -> str:
        """Get AI response from Claude API with conversation memory"""
        api_key = config.ANTHROPIC_API_KEY
        if not api_key:
            return self._fallback_response(user_input)

        # Maintain rolling conversation history
        self.history.append({"role": "user", "content": user_input})
        if len(self.history) > self.max_history * 2:
            self.history = self.history[-self.max_history * 2:]

        try:
            resp = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                },
                json={
                    "model": config.AI_MODEL,
                    "max_tokens": config.AI_MAX_TOKENS,
                    "system": JARVIS_SYSTEM,
                    "messages": self.history
                },
                timeout=30
            )
            data = resp.json()
            if "content" in data and data["content"]:
                reply = data["content"][0]["text"]
                self.history.append({"role": "assistant", "content": reply})
                return reply
            return self._fallback_response(user_input)
        except Exception as e:
            print(f"[AIChat] Error: {e}")
            return self._fallback_response(user_input)

    def clear_history(self):
        self.history = []
        return "Conversation memory cleared, sir."

    def _fallback_response(self, user_input: str) -> str:
        """Rule-based fallback when API is unavailable"""
        low = user_input.lower()
        if any(w in low for w in ["hello", "hi", "hey", "greet"]):
            return "Good day, sir. J.A.R.V.I.S. is fully operational. How may I assist you?"
        if any(w in low for w in ["how are you", "status", "feeling"]):
            return "All systems are operating at peak efficiency, sir. Ready for your commands."
        if "jarvis" in low and any(w in low for w in ["who", "what are you", "about"]):
            return ("I am J.A.R.V.I.S. — Just A Rather Very Intelligent System. "
                    "I am an AI-powered web command center running on Flask and Python, "
                    "designed to assist with commands, information, productivity, and intelligent conversation.")
        if any(w in low for w in ["thanks", "thank you", "good job", "well done"]):
            return "Always a pleasure to be of service, sir."
        if any(w in low for w in ["joke", "funny"]):
            return ("Why don't scientists trust atoms? Because they make up everything. "
                    "Much like my former colleague, sir.")
        return ("I understand your request, sir. However, my cloud intelligence connection is unavailable at the moment. "
                "Please add your ANTHROPIC_API_KEY to the .env file for full AI capabilities. "
                "In the meantime, I can still assist with commands, system actions, and built-in features.")


ai_chat = AIChat()
