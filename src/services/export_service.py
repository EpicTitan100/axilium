"""Data export service."""

import json
import csv
from datetime import datetime, date
from typing import Optional
from pathlib import Path
from ..models.database import Database
from ..models.habit import Habit
from ..models.reward import Reward


class ExportService:
    """Service for exporting data."""
    
    def __init__(self, db: Database):
        """Initialize export service."""
        self.db = db
    
    def export_to_json(self, file_path: str, start_date: Optional[date] = None, end_date: Optional[date] = None):
        """Export all data to JSON format."""
        data = {
            "export_date": datetime.now().isoformat(),
            "habits": [],
            "completions": [],
            "rewards": [],
            "settings": {}
        }
        
        # Export habits
        habits = self.db.get_all_habits()
        for habit in habits:
            habit_dict = habit.to_dict()
            data["habits"].append(habit_dict)
            
            # Export completions for this habit
            completions = self.db.get_completions(habit.id, start_date, end_date)
            for completion_date in completions:
                data["completions"].append({
                    "habit_id": habit.id,
                    "habit_name": habit.name,
                    "completion_date": completion_date.isoformat()
                })
        
        # Export rewards
        rewards = self.db.get_all_rewards()
        for reward in rewards:
            data["rewards"].append(reward.to_dict())
        
        # Export settings
        # Note: This is a simplified version - you might want to export all settings
        theme = self.db.get_setting("theme", "dark")
        data["settings"]["theme"] = theme
        
        # Write to file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def export_to_csv(self, file_path: str, start_date: Optional[date] = None, end_date: Optional[date] = None):
        """Export completion records to CSV."""
        habits = self.db.get_all_habits()
        
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Habit ID", "Habit Name", "Category", "Completion Date", "Streak"])
            
            for habit in habits:
                completions = self.db.get_completions(habit.id, start_date, end_date)
                for completion_date in completions:
                    writer.writerow([
                        habit.id,
                        habit.name,
                        habit.category,
                        completion_date.isoformat(),
                        habit.streak_count
                    ])
    
    def import_from_json(self, file_path: str) -> bool:
        """Import data from JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Import habits
            if "habits" in data:
                for habit_data in data["habits"]:
                    habit = Habit.from_dict(habit_data)
                    if habit.id:
                        # Update existing or create new
                        existing = self.db.get_habit(habit.id)
                        if existing:
                            self.db.update_habit(habit)
                        else:
                            self.db.add_habit(habit)
            
            # Import completions
            if "completions" in data:
                for comp_data in data["completions"]:
                    habit_id = comp_data.get("habit_id")
                    comp_date = date.fromisoformat(comp_data["completion_date"])
                    self.db.add_completion(habit_id, comp_date)
            
            return True
        except Exception as e:
            print(f"Error importing data: {e}")
            return False
