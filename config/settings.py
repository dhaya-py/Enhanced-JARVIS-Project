"""
Configuration Manager for Jarvis AI Assistant
Handles environment variables and system configuration
"""

import os
from pathlib import Path
from dotenv import load_dotenv

class Config:
    """Central configuration class"""
    
    # Base paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    
    def __init__(self):
        # Load environment variables
        env_path = self.BASE_DIR / ".env"
        if env_path.exists():
            load_dotenv(env_path)
        
        # Create necessary directories
        self.DATA_DIR.mkdir(exist_ok=True)
        self.LOGS_DIR.mkdir(exist_ok=True)
        
        # API Keys (optional)
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        self.OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
        
        # Email Configuration
        self.EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "")
        self.EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
        
        # System Settings
        self.DEBUG_MODE = os.getenv("DEBUG_MODE", "True").lower() == "true"
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        
        # Voice Settings
        self.VOICE_TIMEOUT = 5
        self.VOICE_PHRASE_LIMIT = 5
        self.TTS_RATE = 150
        
        # Intent Detection
        self.INTENT_THRESHOLD = 0.5
        self.DATASET_PATH = self.DATA_DIR / "os_dataset.csv"
        
        # Database
        self.DB_PATH = self.DATA_DIR / "jarvis.db"
        
    def has_openai_key(self):
        """Check if OpenAI API key is available"""
        return bool(self.OPENAI_API_KEY and self.OPENAI_API_KEY != "your_openai_api_key_here")
    
    def has_weather_key(self):
        """Check if Weather API key is available"""
        return bool(self.OPENWEATHER_API_KEY and self.OPENWEATHER_API_KEY != "your_openweather_api_key_here")

# Global config instance
config = Config()
