from django.db import models
from django.conf import settings

class Habit(models.Model):
    name = models.CharField(max_length=100) # e.g. "Salah"
    slug = models.SlugField(unique=True) # e.g. "salah"
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    preferences = models.JSONField(default=dict) # {method: 'text', intensity: 'steady', prayers: []}
    created_at = models.DateTimeField(auto_now_add=True)
    last_reminded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'habit')

    def __str__(self):
        return f"{self.user} -> {self.habit}"

class ActivityLog(models.Model):
    STATUS_CHOICES = [
        ('prayed', 'Prayed'),
        ('missed', 'Missed'),
        ('late', 'Late'),
        ('unknown', 'Unknown'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50) # e.g. "fajr"
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    reference_time = models.DateTimeField() # When was the task due?
    logged_at = models.DateTimeField(auto_now_add=True)
    reflection_note = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user} - {self.event_type} - {self.status}"
