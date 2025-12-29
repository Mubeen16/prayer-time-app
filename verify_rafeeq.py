import sys
from datetime import datetime, timedelta
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("RafeeqVerify")

sys.path.append("backend")

from rafeeq import database, users, logs, preferences
from rafeeq.habits.salah import scheduler, confirmation, summary
from rafeeq import dispatcher

def verify_full_stack():
    logger.info("=== RAFEEQ V1 VERIFICATION ===")
    
    # 1. Database
    logger.info("[1/6] Initializing Database...")
    database.init_db()
    
    # 2. Users & Preferences
    logger.info("[2/6] Registering User & Checking Preferences...")
    user_id = users.register_user("+447000000000", "Test User", "Europe/London", 51.5, -0.1)
    users.subscribe_habit(user_id, "salah")
    
    prefs = preferences.get_preferences(user_id)
    logger.info(f"    Preferences loaded: {len(prefs)} keys found.")

    # 3. Scheduler (Al-Vaqth Integration)
    logger.info("[3/6] Testing Salah Scheduler...")
    user = users.get_user_by_phone("+447000000000")
    salah = scheduler.SalahHabit()
    event = salah.get_next_event(user)
    
    if event:
        logger.info(f"    Next Prayer detected: {event['event_type']} at {event['due_at']}")
        logger.info(f"    Reminder: {salah.format_reminder(event)}")
    else:
        logger.warning("    No next prayer found today.")

    # 4. Dispatcher & Confirmation logic
    logger.info("[4/6] Testing Dispatcher (Inbound Message)...")
    # Simulate user sending "prayed"
    try:
        dispatcher.handle_incoming_message("+447000000000", "I prayed thanks")
        # Check logs to confirm it was recorded
        recent_logs = logs.get_logs(user_id, "salah", limit=1)
        if recent_logs and recent_logs[0]['status'] == "prayed":
            logger.info("    Success: 'prayed' status logged database.")
        else:
            logger.error("    Fail: Log not found or incorrect status.")
    except Exception as e:
        logger.error(f"    Dispatcher error: {e}")

    # 5. Summary Generation
    logger.info("[5/6] Testing Nightly Summary...")
    report = summary.generate_daily_summary(user_id)
    logger.info(f"    Summary Generated: \"{report}\"")

    logger.info("=== VERIFICATION COMPLETE ===")

if __name__ == "__main__":
    verify_full_stack()
