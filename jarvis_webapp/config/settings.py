"""
JARVIS Configuration Settings
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent

class Config:
    # API Keys
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")

    # Database
    DATABASE_PATH = BASE_DIR / "data" / "jarvis.db"

    # Intent Detection
    DATASET_PATH = BASE_DIR / "data" / "os_dataset.csv"
    INTENT_THRESHOLD = 0.35

    # App
    DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "jarvis-iron-man-2024")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))

    # AI
    AI_MODEL = "claude-sonnet-4-20250514"
    AI_MAX_TOKENS = 1000

    # Voice
    VOICE_LANGUAGE = "en-IN"
    VOICE_RATE = 175
    VOICE_VOLUME = 0.9

config = Config()
