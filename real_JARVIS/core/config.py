"""
JARVIS PRIME - Core Configuration
Completely isolated from web-app dependencies.
"""
import os
from pathlib import Path
from dataclasses import dataclass

BASE_DIR = Path(__file__).resolve().parent.parent

@dataclass
class PrimeConfig:
    # Network / Daemon Settings
    DAEMON_HOST: str = os.getenv("JARVIS_PRIME_HOST", "127.0.0.1")
    DAEMON_PORT: int = int(os.getenv("JARVIS_PRIME_PORT", 9999))
    
    # Memory Settings
    DB_PATH: Path = BASE_DIR / "memory" / "prime_memory.db"
    
    # Intelligence Settings
    INTENT_THRESHOLD: float = 0.65
    
    # Paths
    DATASET_PATH: Path = BASE_DIR / "engine" / "intent_dataset.csv"

config = PrimeConfig()
