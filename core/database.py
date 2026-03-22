"""
Database Manager for Jarvis AI Assistant
Handles SQLite operations for logging commands and responses
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Optional
from config.settings import config

class DatabaseManager:
    """Manages database operations for Jarvis"""
    
    def __init__(self):
        self.db_path = config.DB_PATH
        self._initialize_database()
    
    def _initialize_database(self):
        """Create database and tables if they don't exist"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        command TEXT NOT NULL,
                        response TEXT NOT NULL,
                        timestamp TEXT NOT NULL
                    )
                """)
                conn.commit()
                if config.DEBUG_MODE:
                    print(f"✓ Database initialized at {self.db_path}")
        except sqlite3.Error as e:
            print(f"✗ Database initialization error: {e}")
    
    def log_interaction(self, command: str, response: str) -> bool:
        """
        Log a command-response interaction
        
        Args:
            command: User's input command
            response: Jarvis's response
            
        Returns:
            True if successful, False otherwise
        """
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO logs (command, response, timestamp)
                    VALUES (?, ?, ?)
                """, (command, response, timestamp))
                conn.commit()
                if config.DEBUG_MODE:
                    print(f"✓ Logged: {command[:30]}... -> {response[:30]}...")
                return True
        except sqlite3.Error as e:
            print(f"✗ Logging error: {e}")
            return False
    
    def get_recent_logs(self, limit: int = 10) -> List[Tuple]:
        """
        Retrieve recent interaction logs
        
        Args:
            limit: Number of recent logs to retrieve
            
        Returns:
            List of tuples (id, command, response, timestamp)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, command, response, timestamp
                    FROM logs
                    ORDER BY id DESC
                    LIMIT ?
                """, (limit,))
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"✗ Error fetching logs: {e}")
            return []
    
    def get_logs_by_date(self, date: str) -> List[Tuple]:
        """
        Get logs for a specific date
        
        Args:
            date: Date in format 'YYYY-MM-DD'
            
        Returns:
            List of tuples (id, command, response, timestamp)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, command, response, timestamp
                    FROM logs
                    WHERE timestamp LIKE ?
                    ORDER BY id DESC
                """, (f"{date}%",))
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"✗ Error fetching logs by date: {e}")
            return []
    
    def clear_logs(self) -> bool:
        """
        Clear all logs from database
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM logs")
                conn.commit()
                print("✓ All logs cleared")
                return True
        except sqlite3.Error as e:
            print(f"✗ Error clearing logs: {e}")
            return False
    
    def get_stats(self) -> dict:
        """
        Get database statistics
        
        Returns:
            Dictionary with stats
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM logs")
                total = cursor.fetchone()[0]
                
                cursor.execute("""
                    SELECT DATE(timestamp) as date, COUNT(*) as count
                    FROM logs
                    GROUP BY date
                    ORDER BY date DESC
                    LIMIT 7
                """)
                daily = cursor.fetchall()
                
                return {
                    "total_interactions": total,
                    "daily_breakdown": daily
                }
        except sqlite3.Error as e:
            print(f"✗ Error getting stats: {e}")
            return {"total_interactions": 0, "daily_breakdown": []}

# Global database instance
db = DatabaseManager()
