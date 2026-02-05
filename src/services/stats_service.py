"""Statistics calculation service."""

from datetime import datetime, date, timedelta
from typing import Dict, List, Tuple
from ..models.database import Database
from ..models.habit import Habit


class StatsService:
    """Service for calculating habit statistics."""
    
    def __init__(self, db: Database):
        """Initialize with database connection."""
        self.db = db
    
    def get_overall_completion_rate(self, days: int = 30) -> float:
        """Calculate overall completion rate for the last N days."""
        habits = self.db.get_all_habits()
        if not habits:
            return 0.0
        
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        total_possible = len(habits) * days
        total_completed = 0
        
        for habit in habits:
            count = self.db.get_completion_count(habit.id, start_date, end_date)
            total_completed += count
        
        if total_possible == 0:
            return 0.0
        
        return (total_completed / total_possible) * 100
    
    def get_average_streak(self) -> float:
        """Calculate average streak length."""
        habits = self.db.get_all_habits()
        if not habits:
            return 0.0
        
        total_streak = sum(habit.streak_count for habit in habits)
        return total_streak / len(habits)
    
    def get_best_performing_habits(self, limit: int = 5) -> List[Habit]:
        """Get habits with highest completion rates."""
        habits = self.db.get_all_habits()
        
        # Calculate completion rate for each habit
        habit_scores = []
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        
        for habit in habits:
            completed = self.db.get_completion_count(habit.id, start_date, end_date)
            if habit.frequency == "daily":
                possible = 30
            else:
                possible = 4
            
            rate = (completed / possible) * 100 if possible > 0 else 0
            habit_scores.append((habit, rate))
        
        # Sort by completion rate
        habit_scores.sort(key=lambda x: x[1], reverse=True)
        return [habit for habit, _ in habit_scores[:limit]]
    
    def get_weekly_summary(self) -> Dict:
        """Get summary for the current week."""
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        
        habits = self.db.get_all_habits()
        total_completions = 0
        
        for habit in habits:
            count = self.db.get_completion_count(habit.id, week_start, week_end)
            total_completions += count
        
        return {
            "start_date": week_start,
            "end_date": week_end,
            "total_habits": len(habits),
            "total_completions": total_completions,
            "habits_completed": len([h for h in habits if self.db.get_completion_count(h.id, week_start, week_end) > 0])
        }
    
    def get_monthly_summary(self) -> Dict:
        """Get summary for the current month."""
        today = date.today()
        month_start = date(today.year, today.month, 1)
        month_end = today
        
        habits = self.db.get_all_habits()
        total_completions = 0
        
        for habit in habits:
            count = self.db.get_completion_count(habit.id, month_start, month_end)
            total_completions += count
        
        return {
            "start_date": month_start,
            "end_date": month_end,
            "total_habits": len(habits),
            "total_completions": total_completions,
            "habits_completed": len([h for h in habits if self.db.get_completion_count(h.id, month_start, month_end) > 0])
        }
    
    def get_category_breakdown(self) -> Dict[str, int]:
        """Get completion count by category."""
        habits = self.db.get_all_habits()
        breakdown = {}
        
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        
        for habit in habits:
            category = habit.category
            if category not in breakdown:
                breakdown[category] = 0
            
            count = self.db.get_completion_count(habit.id, start_date, end_date)
            breakdown[category] += count
        
        return breakdown
    
    def get_completion_trend(self, habit_id: int, days: int = 30) -> List[Tuple[date, bool]]:
        """Get completion trend for a habit over the last N days."""
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        completions = self.db.get_completions(habit_id, start_date, end_date)
        completion_set = set(completions)
        
        trend = []
        current_date = start_date
        while current_date <= end_date:
            trend.append((current_date, current_date in completion_set))
            current_date += timedelta(days=1)
        
        return trend
    
    def get_calendar_heatmap_data(self, days: int = 365) -> Dict[date, int]:
        """Get completion data for calendar heatmap."""
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        habits = self.db.get_all_habits()
        heatmap = {}
        
        current_date = start_date
        while current_date <= end_date:
            heatmap[current_date] = 0
            current_date += timedelta(days=1)
        
        for habit in habits:
            completions = self.db.get_completions(habit.id, start_date, end_date)
            for completion_date in completions:
                if completion_date in heatmap:
                    heatmap[completion_date] += 1
        
        return heatmap
