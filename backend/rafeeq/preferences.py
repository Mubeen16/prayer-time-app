from rafeeq.database import get_connection

DEFAULT_SALAH_PREFERENCES = {
    "fajr": True,
    "zuhr": True,
    "asr": True,
    "maghrib": True,
    "isha": True
}

def get_preferences(user_id: int):
    """
    Get user preferences.
    For V1, we largely rely on defaults or could store JSON in a 'preferences' column if we added one.
    To keep V1 simple and strict to the schema provided:
    We will assume ALL prayers are enabled by default for subscribers.
    Future: Read from a 'preferences' table.
    """
    # Placeholder for future extensibility
    return DEFAULT_SALAH_PREFERENCES.copy()

def update_preference(user_id: int, key: str, value: bool):
    """
    Update a specific preference.
    For V1, this might be a no-op or require schema expansion if we want per-prayer toggles.
    Given constraints, we'll keep it as a stub or simple in-memory check for V1.
    """
    pass
