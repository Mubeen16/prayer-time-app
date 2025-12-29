import sqlite3
import logging
from pathlib import Path
from datetime import datetime

# Set up logging
logger = logging.getLogger(__name__)

DB_PATH = Path("rafeeq.db")

def get_connection():
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Users Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT UNIQUE NOT NULL,
                name TEXT,
                timezone TEXT DEFAULT 'UTC',
                latitude REAL,
                longitude REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Habit Subscriptions Table
        # Tracks which habits a user has opted into (e.g., 'salah')
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habit_subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                habit_id TEXT NOT NULL, -- e.g. 'salah'
                status TEXT DEFAULT 'active', -- active, paused
                subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                preferences TEXT DEFAULT '{}', -- JSON: {prayers: [], method: 'text', intensity: 'steady'}
                last_reminded_event TEXT, -- e.g. 'asr'
                last_reminded_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(user_id, habit_id)
            )
        """)

        # Migration for existing tables (safe add column)
        try:
            cursor.execute("ALTER TABLE habit_subscriptions ADD COLUMN preferences TEXT DEFAULT '{}'")
        except sqlite3.OperationalError:
            pass # Column likely exists

        try:
            cursor.execute("ALTER TABLE habit_subscriptions ADD COLUMN last_reminded_event TEXT")
        except sqlite3.OperationalError:
            pass

        try:
            cursor.execute("ALTER TABLE habit_subscriptions ADD COLUMN last_reminded_at TIMESTAMP")
        except sqlite3.OperationalError:
            pass

        # Logs Table
        # Records the outcome of a habit event
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                habit_id TEXT NOT NULL,
                event_type TEXT NOT NULL, -- e.g. 'fajr', 'zuhr'
                reference_time_utc TIMESTAMP, -- When the event was due
                status TEXT NOT NULL, -- 'prayed', 'missed', 'late'
                logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        conn.commit()
        logger.info("Rafeeq Database initialized successfully.")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_db()
