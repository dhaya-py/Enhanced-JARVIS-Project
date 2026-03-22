"""
Information Module for Jarvis AI Assistant
Handles informational queries (time, date, weather, etc.)
"""

from datetime import datetime
import requests
from typing import Tuple, Optional
from config.settings import config

class InformationProvider:
    """Provides informational responses"""
    
    def __init__(self):
        self.weather_api_key = config.OPENWEATHER_API_KEY if config.has_weather_key() else None
        
        if config.DEBUG_MODE:
            print("✓ Information Provider initialized")
    
    def get_time(self) -> str:
        """Get current time"""
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        return f"The current time is {time_str}"
    
    def get_date(self) -> str:
        """Get current date"""
        now = datetime.now()
        date_str = now.strftime("%B %d, %Y")
        day_str = now.strftime("%A")
        return f"Today is {day_str}, {date_str}"
    
    def get_datetime(self) -> str:
        """Get current date and time"""
        now = datetime.now()
        datetime_str = now.strftime("%A, %B %d, %Y at %I:%M %p")
        return f"It is {datetime_str}"
    
    def get_weather(self, city: str = "London") -> Tuple[bool, str]:
        """
        Get weather information for a city
        
        Args:
            city: City name (default: London)
            
        Returns:
            Tuple of (success, weather_info)
        """
        # If no API key, return stub response
        if not self.weather_api_key:
            return True, self._get_weather_stub(city)
        
        try:
            # OpenWeatherMap API
            base_url = "http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': city,
                'appid': self.weather_api_key,
                'units': 'metric'  # Celsius
            }
            
            response = requests.get(base_url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract weather info
                temp = data['main']['temp']
                feels_like = data['main']['feels_like']
                humidity = data['main']['humidity']
                description = data['weather'][0]['description']
                
                weather_info = (
                    f"Weather in {city}: {description}. "
                    f"Temperature is {temp}°C, feels like {feels_like}°C. "
                    f"Humidity is {humidity}%."
                )
                
                return True, weather_info
            else:
                return False, f"Could not fetch weather for {city}"
                
        except requests.exceptions.Timeout:
            return False, "Weather service request timed out"
        except Exception as e:
            if config.DEBUG_MODE:
                print(f"✗ Weather error: {e}")
            return False, f"Error getting weather information"
    
    def _get_weather_stub(self, city: str) -> str:
        """
        Stub weather response when API key is not available
        
        Args:
            city: City name
            
        Returns:
            Stub weather message
        """
        return (
            f"Weather service is not configured. "
            f"To get real weather data for {city}, please add your OpenWeatherMap API key to the .env file."
        )
    
    def get_about_jarvis(self) -> str:
        """Get information about Jarvis"""
        return (
            "I am Jarvis, your AI-based personal assistant. "
            "I can help you with system tasks, web searches, information queries, and more. "
            "Just tell me what you need, and I'll assist you."
        )
    
    def get_help(self) -> str:
        """Get help message with available commands"""
        help_text = """
Here are some things I can do:

System Commands:
- Open applications (notepad, calculator, chrome, explorer)
- Close windows or applications
- Take screenshots
- Lock, shutdown, restart, or sleep the computer

Web Actions:
- Open websites (youtube, google, facebook, github, etc.)
- Search Google, YouTube, or Wikipedia
- Open any URL

Information:
- Tell you the time and date
- Get weather information
- Answer general questions

Just speak naturally, and I'll understand what you need!
        """
        return help_text.strip()
    
    def acknowledge(self) -> str:
        """Acknowledge user's thanks or praise"""
        responses = [
            "You're welcome!",
            "Happy to help!",
            "My pleasure!",
            "Anytime!",
            "Glad I could assist!",
        ]
        import random
        return random.choice(responses)

# Global information provider instance
info_provider = InformationProvider()
