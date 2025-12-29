from datetime import datetime
from rafeeq import logs

def process_confirmation(user_id: int, message_body: str, reference_time_utc: datetime):
    """
    Parses user message to determine Salah status and logs it.
    V1 Logic:
    - "prayed", "done", "yes" -> Status: 'prayed'
    - "missed", "no" -> Status: 'missed'
    - Default -> Status: 'unknown' (or ignore)
    """
    msg = message_body.lower().strip()
    status = "unknown"
    
    if any(alias in msg for alias in ["prayed", "done", "yes", "alhamdulillah"]):
        status = "prayed"
    elif any(alias in msg for alias in ["missed", "no", "not yet"]):
        status = "missed"
    
    if status != "unknown":
        # Log the event
        # Logic assumption: The habit identifies which prayer this is for before calling this.
        # But for V1 simplification, we might log it here or return the status.
        # To strictly follow "confirmation.py" handling logic:
        # We need the habit_id and event_type passed in or inferred.
        # Let's return the status so the caller (HabitBase.handle_response) can log it with full context.
        return status
    
    return None
