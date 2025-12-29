from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo
from rafeeq.habits.base import HabitBase
from rafeeq.habits.salah import confirmation
from rafeeq import logs
from core.prayer_times import get_prayer_times

class SalahHabit(HabitBase):
    @property
    def habit_id(self):
        return "salah"

    def get_next_event(self, user_row) -> dict:
        """
        Determines the NEXT prayer time for the user based on Al-Vaqth core.
        """
        lat = user_row['latitude']
        lng = user_row['longitude']
        tz_str = user_row['timezone']
        
        if not lat or not lng:
            return None

        # 1. Get times for today
        today = date.today()
        user_tz = ZoneInfo(tz_str)
        now_user = datetime.now(user_tz)
        
        # Fetch Al-Vaqth times
        data_today = get_prayer_times(
            latitude=lat, 
            longitude=lng, 
            on_date=today, 
            timezone=tz_str
        )
        
        # Parse times into comparable datetimes
        events = []
        for name, time_str in data_today['times'].items():
            dt_str = f"{data_today['date']} {time_str}"
            dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M").replace(tzinfo=user_tz)
            events.append((name, dt))
            
        events.sort(key=lambda x: x[1])
        
        # Find first event in the future
        for name, dt in events:
            if dt > now_user:
                return {
                    'event_type': name,
                    'due_at': dt, # datetime with tzinfo
                    'habit_id': self.habit_id
                }
                
        return None

    def format_reminder(self, event) -> str:
        prayer_name = event['event_type'].capitalize()
        # Adab: Simple, direct, no pressure.
        return f"It is time for {prayer_name}."

    def handle_response(self, user_row, message_body: str):
        """
        Process user response.
        Uses confirmation logic to determine status.
        Logs the event if valid status found.
        """
        # For V1, we don't know exact 'reference_time' from the message alone
        # so we log strictly based on 'now' or most recent prayer?
        # A robust system would track 'last_reminded_event'.
        # For V1 simple prototype, let's assume they are replying to the most recent prayer passed.
        
        # 1. Identify status
        # We pass a dummy time for now as V1 confirmation logic helps identify status string
        status = confirmation.process_confirmation(user_row['id'], message_body, datetime.now())
        
        if status:
            # 2. Log it
            # We need to find *what* they are confirming. 
            # Simplified: Log it as a generic 'response' or try to find the previous prayer.
            # Let's assume most recent past prayer.
            # (Re-using get_next_event logic but looking backward would be ideal)
            # For V1 prototype: Just log with event_type='unknown/manual' or similar if not tracking state.
            
            logs.log_event(
                user_id=user_row['id'],
                habit_id=self.habit_id,
                event_type="manual_entry", # placeholder for V1 stateless
                reference_time_utc=datetime.utcnow(),
                status=status
            )
            
            if status == "prayed":
                return "Alhamdulillah. Recorded."
            elif status == "missed":
                return "Recorded. May Allah make it easy for you."
                
        return None
