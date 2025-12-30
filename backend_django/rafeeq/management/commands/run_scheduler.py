from django.core.management.base import BaseCommand
import time
from users.models import User
from rafeeq.services import SalahService

class Command(BaseCommand):
    help = 'Runs the Rafeeq Intervention Scheduler (Loop)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Rafeeq Scheduler...'))
        
        while True:
            try:
                self.check_interventions()
                # Sleep for 60 seconds
                time.sleep(60)
            except KeyboardInterrupt:
                self.stdout.write(self.style.WARNING('\nStopping Scheduler...'))
                break
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error in scheduler loop: {e}'))
                time.sleep(60) # Wait before retrying

    def check_interventions(self):
        """
        Check all active users for upcoming interventions.
        """
        # In production, use batching or celery tasks
        users = User.objects.all()
        
        for user in users:
            try:
                event = SalahService.get_upcoming_event(user)
                if not event:
                    continue
                
                # Check if event is "Now" (within 2 minute window for demo)
                # In real prod: Check "10 mins before" vs "Now" vs "10 mins after"
                
                # For Phase 1 Demo: Just log what we WOULD do
                self.stdout.write(f"User {user.phone_number}: Event {event['event_type']} due at {event['due_at'].strftime('%H:%M')}. Action: {event['action'].upper()}")
                
                if event['action'] == 'call':
                    # TODO: Trigger Vapi/Twilio Call
                    pass
                elif event['action'] == 'text':
                    # TODO: Trigger WhatsApp Text
                    pass
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error checking user {user.username}: {e}"))
