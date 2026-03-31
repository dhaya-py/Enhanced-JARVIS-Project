"""
JARVIS Information Module — time, date, weather, system info
"""
from datetime import datetime
import requests
from config.settings import config


class InfoProvider:

    def get_time(self) -> str:
        now = datetime.now()
        t = now.strftime("%I:%M:%S %p")
        return f"The current time is {t}, sir."

    def get_date(self) -> str:
        now = datetime.now()
        d = now.strftime("%A, %d %B %Y")
        return f"Today is {d}, sir."

    def get_datetime(self) -> str:
        now = datetime.now()
        return f"It is {now.strftime('%I:%M %p')} on {now.strftime('%A, %d %B %Y')}, sir."

    def get_weather(self, city: str = "Chennai") -> str:
        key = config.OPENWEATHER_API_KEY
        if not key:
            return self._weather_fallback(city)
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
            r = requests.get(url, timeout=8)
            data = r.json()
            if data.get("cod") == 200:
                temp = data["main"]["temp"]
                feels = data["main"]["feels_like"]
                desc = data["weather"][0]["description"].title()
                humidity = data["main"]["humidity"]
                wind = data["wind"]["speed"]
                city_name = data["name"]
                return (f"Weather in {city_name}: {desc}, {temp:.1f}°C "
                        f"(feels like {feels:.1f}°C). "
                        f"Humidity: {humidity}%, Wind: {wind} m/s, sir.")
            return self._weather_fallback(city)
        except Exception as e:
            return self._weather_fallback(city)

    def _weather_fallback(self, city: str) -> str:
        return (f"Weather service is currently offline, sir. "
                f"Please add an OPENWEATHER_API_KEY to your .env file "
                f"for live weather data for {city}.")

    def get_about_jarvis(self) -> str:
        return ("I am J.A.R.V.I.S. — Just A Rather Very Intelligent System, version 3.0. "
                "I am an advanced AI-powered web command center built with Python, Flask, and WebSocket technology. "
                "I feature voice input/output, intent detection, system automation, AI conversation, "
                "productivity management, and real-time monitoring. "
                "How may I be of further service, sir?")

    def get_help(self) -> str:
        return """Available command categories:

⚙ SYSTEM: open/close apps, screenshot, lock screen, volume, shutdown, restart
🌐 WEB: open YouTube/GitHub/LinkedIn, Google search, open any website
ℹ INFO: time, date, weather [city], system info, about JARVIS
📝 NOTES: add note [text], show notes, clear notes
✅ TASKS: add task [text], show tasks, show pending tasks
🔔 REMINDERS: remind me [text], show reminders
🧮 MATH: calculate [expression], convert [unit] to [unit]
🌍 TRANSLATE: translate [text] to [language]
📰 NEWS: latest news, tech news, sports news, world news
🔍 KNOWLEDGE: who is [person], what is [topic], define [word]
😄 FUN: tell me a joke, give me a quote, fun fact, trivia
🔐 SECURITY: generate password [length]
📊 ANALYSIS: analyze sentiment [text], summarize [text]
🗣 VOICE: click the mic or Arc Reactor to use voice commands

For any question, just ask — my AI engine will handle it."""

    def acknowledge(self) -> str:
        import random
        responses = [
            "Always at your service, sir.",
            "My pleasure, sir.",
            "You're most welcome. Anything else?",
            "Happy to be of assistance, sir.",
            "Of course, sir. That's what I'm here for."
        ]
        return random.choice(responses)


info_provider = InfoProvider()
