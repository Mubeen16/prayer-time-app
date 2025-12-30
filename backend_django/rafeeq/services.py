from datetime import datetime, date as Date
from zoneinfo import ZoneInfo
from core.prayer_times import get_prayer_times
from .models import Habit, Subscription

class SalahService:
    @staticmethod
    def get_upcoming_event(user):
        """
        Logic:
        1. Fetch prayer times for user.
        2. Filter by user's subscribed prayers.
        3. Identify the NEXT upcoming prayer.
        4. Return event metadata + method info (Call/Text).
        """
        # Default Settings
        DEFAULT_PRAYERS = ['fajr', 'zuhr', 'asr', 'maghrib', 'isha']
        
        # 1. Get User Preferences
        try:
            subscription = Subscription.objects.get(user=user, habit__slug="salah", is_active=True)
            prefs = subscription.preferences or {}
        except Subscription.DoesNotExist:
            return None # Not subscribed
            
        selected_prayers = prefs.get('prayers', DEFAULT_PRAYERS)
        if not selected_prayers:
             selected_prayers = DEFAULT_PRAYERS
             
        # 2. Calculate Times
        today = datetime.now().date()
        try:
             # Basic timezone handling: assumes timezone is valid
             times_data = get_prayer_times(
                latitude=user.latitude or 0.0,
                longitude=user.longitude or 0.0,
                on_date=today,
                timezone=user.timezone or "UTC"
            )
        except Exception as e:
            # Fallback for invalid calculation params
            return None

        # 3. Parse and Find Next Event
        now_user = datetime.now(ZoneInfo(user.timezone))
        events = []
        
        for name, time_str in times_data['times'].items():
            if name.lower() not in selected_prayers:
                continue
                
            # Create aware datetime for prayer
            dt_str = f"{times_data['date']} {time_str}"
            dt_naive = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
            dt_aware = dt_naive.replace(tzinfo=ZoneInfo(user.timezone))
            
            events.append((name, dt_aware))
            
        events.sort(key=lambda x: x[1])
        
        # Find first future event
        for name, dt in events:
            if dt > now_user:
                return {
                    'event_type': name,
                    'due_at': dt,
                    'action': prefs.get('method', 'text'),
                    'intensity': prefs.get('intensity', 'steady')
                }
                
        # TODO: Handle "Next Day Fajr" lookup if no events left today
        return None
