from datetime import datetime, time, timedelta

def parse_time(t_str):
    """Parses HH:MM string to time object."""
    return datetime.strptime(t_str, "%H:%M").time()

def calculate_schedule(tasks, prayer_times):
    """
    Generates a schedule by placing tasks into 'Barakah Blocks' defined by prayer times.
    
    Args:
        tasks: List of dicts {'name': str, 'duration_minutes': int, 'type': 'deep'|'shallow'}
        prayer_times: Dict output from get_prayer_times()
    
    Returns:
        List of dicts representing the schedule blocks.
    """
    
    # Extract times
    times = prayer_times['times']
    fajr = parse_time(times['fajr'])
    sunrise = parse_time(times['sunrise'])
    zuhr = parse_time(times['zuhr'])
    asr = parse_time(times['asr'])
    maghrib = parse_time(times['maghrib'])
    isha = parse_time(times['isha'])
    
    schedule = []
    
    # 1. Fajr - Sunrise (The "Barakah" Hour)
    schedule.append({
        "period": "Early Morning (Barakah Hour)",
        "start": times['fajr'],
        "end": times['sunrise'],
        "suggested_activity": "Spiritual reading, Quran, or Planning the day.",
        "type": "spiritual"
    })
    
    # 2. Sunrise - Zuhr (Deep Work)
    # This is usually the longest block. Good for hard tasks.
    schedule.append({
        "period": "Morning Deep Work",
        "start": times['sunrise'],
        "end": times['zuhr'],
        "suggested_activity": "Deep Work. Tackle your hardest task here.",
        "type": "work_deep",
        "tasks": [t for t in tasks if t.get('type') == 'deep']
    })
    
    # 3. Zuhr - Asr (Mid-Day Push)
    schedule.append({
        "period": "Mid-Day Block",
        "start": times['zuhr'],
        "end": times['asr'],
        "suggested_activity": "Meetings, Emails, Admin tasks.",
        "type": "work_shallow",
        "tasks": [t for t in tasks if t.get('type') != 'deep']
    })
    
    # 4. Asr - Maghrib (Wrap Up)
    schedule.append({
        "period": "Late Afternoon",
        "start": times['asr'],
        "end": times['maghrib'],
        "suggested_activity": "Wrap up work. Exercise. Family time.",
        "type": "personal"
    })
    
    # 5. Maghrib - Isha (Community/Family)
    schedule.append({
        "period": "Evening Connection",
        "start": times['maghrib'],
        "end": times['isha'],
        "suggested_activity": "Dinner, Family, Community.",
        "type": "social"
    })
    
    return schedule
