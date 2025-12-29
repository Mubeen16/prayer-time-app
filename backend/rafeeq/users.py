from datetime import datetime
from rafeeq.database import get_connection

def get_user_by_phone(phone_number: str):
    """Retrieve a user by phone number."""
    conn = get_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE phone_number = ?", 
        (phone_number,)
    ).fetchone()
    conn.close()
    return user

def register_user(phone_number: str, name: str, timezone: str, lat: float, lng: float):
    """Register a new user or update an existing one."""
    conn = get_connection()
    try:
        # Upsert logic (simplified for SQLite)
        existing = conn.execute("SELECT id FROM users WHERE phone_number = ?", (phone_number,)).fetchone()
        
        if existing:
            conn.execute("""
                UPDATE users 
                SET name = ?, timezone = ?, latitude = ?, longitude = ?
                WHERE phone_number = ?
            """, (name, timezone, lat, lng, phone_number))
            user_id = existing['id']
        else:
            cursor = conn.execute("""
                INSERT INTO users (phone_number, name, timezone, latitude, longitude)
                VALUES (?, ?, ?, ?, ?)
            """, (phone_number, name, timezone, lat, lng))
            user_id = cursor.lastrowid
            
        conn.commit()
        return user_id
    finally:
        conn.close()

import json

def subscribe_habit(user_id: int, habit_id: str = "salah", preferences: dict = None):
    """Subscribe a user to a habit with preferences."""
    conn = get_connection()
    pref_json = json.dumps(preferences or {})
    try:
        # Check if already exists to update prefs
        conn.execute("""
            INSERT INTO habit_subscriptions (user_id, habit_id, status, preferences)
            VALUES (?, ?, 'active', ?)
            ON CONFLICT(user_id, habit_id) DO UPDATE SET
            status = 'active',
            preferences = excluded.preferences
        """, (user_id, habit_id, pref_json))
        conn.commit()
    finally:
        conn.close()

def get_active_users(habit_id: str = "salah"):
    """Get all users subscribed to a specific habit."""
    conn = get_connection()
    users = conn.execute("""
        SELECT u.* FROM users u
        JOIN habit_subscriptions s ON u.id = s.user_id
        WHERE s.habit_id = ? AND s.status = 'active'
    """, (habit_id,)).fetchall()
    conn.close()
    return users
