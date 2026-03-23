"""
AI Chat Module - Intelligent conversation with memory
Uses rule-based patterns + DuckDuckGo Instant Answers
"""

import random
import re
import requests
from datetime import datetime

class AIChat:
    """Intelligent chatbot with conversation memory"""

    def __init__(self):
        self.conversation_history = []
        self.max_history = 20

        self.patterns = {
            r'\b(hello|hi|hey|greetings|howdy)\b': [
                "Hello! How can I assist you today?",
                "Hey there! What can I do for you?",
                "Hi! I'm Jarvis, your AI assistant. How may I help?",
                "Greetings! Ready to help with anything you need.",
            ],
            r'\bhow are you\b': [
                "I'm functioning at optimal capacity! How can I help you?",
                "All systems operational! What do you need?",
                "Running smooth as always. What's on your mind?",
            ],
            r'\b(your name|who are you)\b': [
                "I'm J.A.R.V.I.S. — Just A Rather Very Intelligent System. Your personal AI assistant.",
                "I'm Jarvis, your AI command center. Think of me as your digital right hand.",
            ],
            r'\b(thank|thanks|thx)\b': [
                "You're welcome! Always happy to help.",
                "My pleasure! Anything else you need?",
                "Glad I could help! 🙂",
            ],
            r'\b(bye|goodbye|see you|later)\b': [
                "Goodbye! I'll be here whenever you need me.",
                "See you later! Don't hesitate to call.",
                "Until next time! Stay awesome. 👋",
            ],
            r'\b(what can you do|capabilities|features|help)\b': [
                ("I can help with many things:\n"
                 "🧠 Answer questions & chat\n"
                 "💻 Control your system (open apps, screenshots, etc.)\n"
                 "🌐 Search the web, open websites\n"
                 "📝 Take notes & manage reminders\n"
                 "📊 Analyze sentiment in text\n"
                 "📰 Fetch latest news\n"
                 "🔢 Calculate math expressions\n"
                 "🌍 Translate languages\n"
                 "📋 Manage tasks & to-do lists\n"
                 "🎮 Tell jokes, quotes & fun facts\n"
                 "🔑 Generate secure passwords\n"
                 "📁 Search files on your computer\n"
                 "Just ask naturally!"),
            ],
            r'\b(bored|nothing to do|entertain)\b': [
                "Try saying 'tell me a joke' or 'fun fact' or 'trivia'!",
                "How about a motivational quote? Just say 'motivate me'!",
                "Want to play trivia? Say 'trivia game'!",
            ],
            r'\b(good morning)\b': [
                "Good morning! ☀️ Ready to make today productive?",
                "Morning! Say 'briefing' to get your daily summary!",
            ],
            r'\b(good night|goodnight)\b': [
                "Good night! 🌙 Rest well, I'll keep watch.",
                "Sweet dreams! I'll be right here when you wake up.",
            ],
            r'\b(i feel|feeling|mood)\b.*(sad|down|depressed|unhappy)': [
                "I'm sorry you're feeling that way. Remember, tough times don't last! 💪",
                "It's okay to feel down sometimes. Take a deep breath. You've got this! 🌟",
                "Would you like to hear a motivational quote? Just say 'motivate me'.",
            ],
            r'\b(i feel|feeling|mood)\b.*(happy|great|good|wonderful|amazing)': [
                "That's wonderful to hear! 🎉 Keep that positive energy going!",
                "Awesome! Happiness is contagious. What made your day great?",
            ],
        }

    def get_response(self, text: str) -> str:
        """Get an intelligent response"""
        # Try pattern matching first
        text_lower = text.lower()

        for pattern, responses in self.patterns.items():
            if re.search(pattern, text_lower):
                response = random.choice(responses)
                self._add_to_history(text, response)
                return response

        # Try DuckDuckGo Instant Answers
        try:
            ddg_response = self._search_duckduckgo(text)
            if ddg_response:
                self._add_to_history(text, ddg_response)
                return ddg_response
        except:
            pass

        # Default response
        defaults = [
            f"I'm not sure about that, but I'm always learning! Try asking something else.",
            "Interesting question! I don't have a specific answer, but try searching the web for more info.",
            "I'd love to help with that. Could you rephrase or try a different command?",
            "That's beyond my current knowledge. Say 'help' to see what I can do!",
        ]
        response = random.choice(defaults)
        self._add_to_history(text, response)
        return response

    def _search_duckduckgo(self, query: str) -> str:
        """Search DuckDuckGo Instant Answers API (free, no key needed)"""
        try:
            url = "https://api.duckduckgo.com/"
            params = {'q': query, 'format': 'json', 'no_html': 1, 'skip_disambig': 1}
            response = requests.get(url, params=params, timeout=5)

            if response.status_code == 200:
                data = response.json()

                # Check Abstract
                if data.get('Abstract'):
                    return f"📖 {data['Abstract']}\n— Source: {data.get('AbstractSource', 'DuckDuckGo')}"

                # Check Answer
                if data.get('Answer'):
                    return f"💡 {data['Answer']}"

                # Check Definition
                if data.get('Definition'):
                    return f"📝 {data['Definition']}"

        except:
            pass
        return None

    def _add_to_history(self, user_msg, bot_msg):
        """Add to conversation history"""
        self.conversation_history.append({
            'user': user_msg,
            'bot': bot_msg,
            'time': datetime.now().strftime('%H:%M:%S')
        })
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)

ai_chat = AIChat()
