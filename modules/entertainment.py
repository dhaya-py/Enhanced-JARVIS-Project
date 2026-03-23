"""
Entertainment Module
Jokes, quotes, fun facts, trivia
"""

import random
import requests

class Entertainment:
    """Fun and entertainment features"""

    def __init__(self):
        self.jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs! 🪲",
            "Why was the JavaScript developer sad? Because he didn't Node how to Express himself!",
            "What's a computer's favorite snack? Microchips! 🍟",
            "Why do Java developers wear glasses? Because they can't C#! 👓",
            "How many programmers does it take to change a light bulb? None. That's a hardware problem!",
            "Why did the programmer quit his job? Because he didn't get arrays! 😄",
            "A SQL query walks into a bar, walks up to two tables and asks... 'Can I JOIN you?'",
            "There are only 10 types of people in the world: those who understand binary and those who don't.",
            "Why do Python programmers have low self-esteem? They're constantly comparing themselves to others.",
            "What's the object-oriented way to become wealthy? Inheritance! 💰",
            "Why did the developer go broke? Because he used up all his cache!",
            "What do you call a bear with no teeth? A gummy bear! 🐻",
            "Why don't scientists trust atoms? Because they make up everything!",
            "What do you call a fake noodle? An impasta! 🍝",
            "Why did the scarecrow win an award? He was outstanding in his field! 🌾",
        ]

        self.quotes = [
            "\"The only way to do great work is to love what you do.\" — Steve Jobs",
            "\"Innovation distinguishes between a leader and a follower.\" — Steve Jobs",
            "\"The future belongs to those who believe in the beauty of their dreams.\" — Eleanor Roosevelt",
            "\"It does not matter how slowly you go as long as you do not stop.\" — Confucius",
            "\"Success is not final, failure is not fatal: it is the courage to continue that counts.\" — Winston Churchill",
            "\"The best time to plant a tree was 20 years ago. The second best time is now.\" — Chinese Proverb",
            "\"Your time is limited, don't waste it living someone else's life.\" — Steve Jobs",
            "\"Believe you can and you're halfway there.\" — Theodore Roosevelt",
            "\"The only impossible journey is the one you never begin.\" — Tony Robbins",
            "\"In the middle of difficulty lies opportunity.\" — Albert Einstein",
            "\"Stay hungry, stay foolish.\" — Steve Jobs",
            "\"Code is like humor. When you have to explain it, it's bad.\" — Cory House",
            "\"First, solve the problem. Then, write the code.\" — John Johnson",
            "\"Sometimes it pays to stay in bed on Monday, rather than spending the rest of the week debugging Monday's code.\" — Dan Salomon",
            "\"Talk is cheap. Show me the code.\" — Linus Torvalds",
        ]

        self.fun_facts = [
            "🧠 The first computer bug was an actual bug — a moth found in a Harvard computer in 1947!",
            "🌐 The first website ever created is still online: info.cern.ch",
            "💾 The first 1GB hard drive (1980) weighed 550 pounds and cost $40,000!",
            "🔌 The QWERTY keyboard was designed to SLOW DOWN typing to prevent typewriter jams.",
            "📧 The first email was sent by Ray Tomlinson to himself in 1971.",
            "🤖 The word 'robot' comes from the Czech word 'robota' meaning 'forced labor'.",
            "🌍 There are more possible iterations of a game of chess than atoms in the known universe.",
            "💡 Alan Turing, the father of computer science, was also an Olympic-level marathon runner.",
            "📱 The first mobile phone call was made on April 3, 1973, by Martin Cooper of Motorola.",
            "🎮 The PlayStation 1 had more computing power than the NASA computers that put man on the moon.",
            "🔢 A group of flamingos is called a 'flamboyance'! 🦩",
            "🐙 Octopuses have three hearts and blue blood!",
            "🍯 Honey never spoils. 3000-year-old honey found in Egyptian tombs was still edible!",
            "⚡ A bolt of lightning is 5 times hotter than the surface of the sun!",
            "🌊 There's enough water in Lake Superior to cover all of North and South America in one foot of water!",
        ]

        self.trivia_questions = [
            {"q": "What is the most used programming language in the world?", "a": "JavaScript", "options": ["Python", "JavaScript", "Java", "C++"]},
            {"q": "Who is known as the father of the Internet?", "a": "Vint Cerf", "options": ["Tim Berners-Lee", "Vint Cerf", "Steve Jobs", "Bill Gates"]},
            {"q": "What does CPU stand for?", "a": "Central Processing Unit", "options": ["Computer Personal Unit", "Central Processing Unit", "Central Program Utility", "Core Processing Unit"]},
            {"q": "In which year was Python first released?", "a": "1991", "options": ["1989", "1991", "1995", "2000"]},
            {"q": "What does HTML stand for?", "a": "HyperText Markup Language", "options": ["HyperText Markup Language", "High Tech Modern Language", "Hyper Transfer Markup Language", "Home Tool Markup Language"]},
            {"q": "Which planet is known as the Red Planet?", "a": "Mars", "options": ["Venus", "Mars", "Jupiter", "Saturn"]},
            {"q": "What is the capital of Japan?", "a": "Tokyo", "options": ["Osaka", "Kyoto", "Tokyo", "Hiroshima"]},
            {"q": "How many bits are in a byte?", "a": "8", "options": ["4", "8", "16", "32"]},
        ]

    def get_joke(self) -> str:
        """Get a random joke, try online first"""
        try:
            response = requests.get("https://official-joke-api.appspot.com/random_joke", timeout=3)
            if response.status_code == 200:
                data = response.json()
                return f"😂 {data['setup']}\n\n{data['punchline']}"
        except:
            pass
        return f"😂 {random.choice(self.jokes)}"

    def get_quote(self) -> str:
        """Get a motivational quote"""
        return f"💫 {random.choice(self.quotes)}"

    def get_quote_short(self) -> str:
        """Get a short quote for briefings"""
        quote = random.choice(self.quotes)
        return quote[:100] + "..." if len(quote) > 100 else quote

    def get_fun_fact(self) -> str:
        """Get a random fun fact"""
        return random.choice(self.fun_facts)

    def get_trivia(self) -> str:
        """Get a trivia question"""
        q = random.choice(self.trivia_questions)
        options = q['options'].copy()
        random.shuffle(options)

        text = f"🎯 Trivia Time!\n\n{q['q']}\n\n"
        for i, opt in enumerate(options, 1):
            text += f"  {i}. {opt}\n"
        text += f"\n💡 Answer: {q['a']}"
        return text

entertainment = Entertainment()
