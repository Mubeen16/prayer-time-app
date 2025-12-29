from rafeeq import logs

def generate_daily_summary(user_id: int):
    """
    Generates a short, text-based summary of today's Salah performance.
    """
    # 1. Fetch logs for today (simplified query limit for V1)
    # Ideally filtering by date, but getting last 5 events is a decent proxy for "today" in V1 prototyp.
    recent_logs = logs.get_logs(user_id, "salah", limit=5)
    
    if not recent_logs:
        return "No Salah logged today. Tomorrow is a new beginning."
        
    prayed_count = sum(1 for log in recent_logs if log['status'] == 'prayed')
    total_count = len(recent_logs)
    
    # Adab: Encouraging, factual.
    if prayed_count == 5:
        return "Alhamdulillah, you completed 5/5 prayers today. May Allah accept your efforts."
    elif prayed_count > 0:
        return f"You completed {prayed_count}/5 prayers today. Keep striving."
    else:
        return "A new day awaits. Bismillah."
