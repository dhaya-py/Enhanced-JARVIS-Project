"""
JARVIS PRIME - Memory Manager
Standalone SQLite database for persistent intelligence and operation logging.
"""
import sqlite3
from datetime import datetime
from pathlib import Path
import json

from core.config import config

class PrimeMemory:
    def __init__(self):
        self.db_path = config.DB_PATH
        self._ensure_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def _ensure_db(self):
        """Initialize the prime memory database schema."""
        if not self.db_path.parent.exists():
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            
        with self._get_conn() as conn:
            cursor = conn.cursor()
            # Execution Log: Every action the daemon takes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS execution_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    command TEXT,
                    intent TEXT,
                    status TEXT,
                    response TEXT
                )
            ''')
            # Knowledge State: Persistent facts/state variables learned
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_state (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at TEXT
                )
            ''')
            conn.commit()

    def log_execution(self, command: str, intent: str, status: str, response: str):
        """Records a daemon execution cycle."""
        with self._get_conn() as conn:
            conn.execute(
                "INSERT INTO execution_log (timestamp, command, intent, status, response) VALUES (?, ?, ?, ?, ?)",
                (datetime.now().isoformat(), command, intent, status, response)
            )
            conn.commit()

    def set_state(self, key: str, value: any):
        """Store a persistent state variable."""
        val_str = json.dumps(value)
        with self._get_conn() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO system_state (key, value, updated_at) VALUES (?, ?, ?)",
                (key, val_str, datetime.now().isoformat())
            )
            conn.commit()

    def get_state(self, key: str) -> any:
        """Retrieve a persistent state variable."""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM system_state WHERE key = ?", (key,))
            row = cursor.fetchone()
            if row:
                return json.loads(row[0])
            return None

memory = PrimeMemory()
