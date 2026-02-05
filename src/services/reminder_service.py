"""Reminder service for habit notifications."""

import threading
import schedule
import time
from datetime import datetime
from typing import Callable, Optional
from ..models.database import Database
from ..models.habit import Habit


class ReminderService:
    """Service for managing habit reminders."""
    
    def __init__(self, db: Database, notification_callback: Optional[Callable] = None):
        """Initialize reminder service."""
        self.db = db
        self.notification_callback = notification_callback
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self._schedule_reminders()
    
    def _schedule_reminders(self):
        """Schedule all active reminders."""
        schedule.clear()
        habits = self.db.get_all_habits()
        
        for habit in habits:
            if habit.reminder_enabled and habit.reminder_time:
                try:
                    schedule.every().day.at(habit.reminder_time).do(
                        self._send_reminder, habit.id
                    )
                except Exception as e:
                    print(f"Error scheduling reminder for habit {habit.id}: {e}")
    
    def _send_reminder(self, habit_id: int):
        """Send a reminder notification for a habit."""
        habit = self.db.get_habit(habit_id)
        if habit and self.notification_callback:
            message = f"Time to {habit.name}! 🔥 Streak: {habit.streak_count} days"
            self.notification_callback(habit.name, message)
    
    def start(self):
        """Start the reminder service."""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop the reminder service."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
    
    def _run(self):
        """Run the reminder scheduler loop."""
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def update_reminders(self):
        """Update reminder schedule (call when habits change)."""
        self._schedule_reminders()
