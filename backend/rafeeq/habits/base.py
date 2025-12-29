from abc import ABC, abstractmethod

class HabitBase(ABC):
    """
    Abstract Base Class for all Rafeeq Habits.
    Enforces a strict interface for Scheduling, Reminding, and Logging.
    """
    
    @property
    @abstractmethod
    def habit_id(self) -> str:
        """Unique identifier for the habit (e.g., 'salah')."""
        pass

    @abstractmethod
    def get_next_event(self, user_row) -> dict:
        """
        Calculate the next scheduled event for this user.
        Must return a dict with: {'event_type': str, 'due_at': datetime}
        or None if no event is pending.
        """
        pass

    @abstractmethod
    def format_reminder(self, event) -> str:
        """
        Return the exact text message to send to the user via WhatsApp.
        Must adhere to Adab constraints (polite, short, no guilt).
        """
        pass

    @abstractmethod
    def handle_response(self, user_row, message_body: str):
        """
        Process an incoming message from the user.
        Should interpret confirmation/missed status and log it.
        """
        pass
