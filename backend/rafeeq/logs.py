from datetime import datetime
from rafeeq.database import get_connection

def log_event(user_id: int, habit_id: str, event_type: str, reference_time_utc: datetime, status: str):
    """
    Log a habit event outcome.
    
    Args:
        user_id: ID of the user.
        habit_id: The habit (e.g. 'salah').
        event_type: Specific event (e.g. 'fajr').
        reference_time_utc: When the event was due.
        status: 'prayed', 'missed', 'late', etc.
    """
    conn = get_connection()
    try:
        conn.execute("""
            INSERT INTO logs (user_id, habit_id, event_type, reference_time_utc, status)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, habit_id, event_type, reference_time_utc, status))
        conn.commit()
    finally:
        conn.close()

def get_logs(user_id: int, habit_id: str, limit: int = 10):
    """Retrieve recent logs for a user/habit."""
    conn = get_connection()
    logs = conn.execute("""
        SELECT * FROM logs 
        WHERE user_id = ? AND habit_id = ? 
        ORDER BY reference_time_utc DESC 
        LIMIT ?
    """, (user_id, habit_id, limit)).fetchall()
    conn.close()
    return logs
