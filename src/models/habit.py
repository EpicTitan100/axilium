"""Habit data model."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Habit:
    """Represents a habit to track."""
    
    id: Optional[int]
    name: str
    description: str
    category: str
    color: str
    icon: str
    frequency: str  # daily, weekly, custom
    streak_count: int
    longest_streak: int
    created_date: datetime
    last_completed_date: Optional[datetime]
    goal_days_per_week: int
    goal_days_per_month: int
    reward_points: int
    reminder_time: Optional[str]  # HH:MM format
    reminder_enabled: bool
    
    def __post_init__(self):
        """Initialize default values."""
        if self.id is None:
            self.id = 0
        if self.streak_count is None:
            self.streak_count = 0
        if self.longest_streak is None:
            self.longest_streak = 0
        if self.created_date is None:
            self.created_date = datetime.now()
        if self.goal_days_per_week is None:
            self.goal_days_per_week = 7 if self.frequency == "daily" else 1
        if self.goal_days_per_month is None:
            self.goal_days_per_month = 30 if self.frequency == "daily" else 4
        if self.reward_points is None:
            self.reward_points = 0
        if self.reminder_enabled is None:
            self.reminder_enabled = False
    
    def to_dict(self) -> dict:
        """Convert habit to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "color": self.color,
            "icon": self.icon,
            "frequency": self.frequency,
            "streak_count": self.streak_count,
            "longest_streak": self.longest_streak,
            "created_date": self.created_date.isoformat(),
            "last_completed_date": self.last_completed_date.isoformat() if self.last_completed_date else None,
            "goal_days_per_week": self.goal_days_per_week,
            "goal_days_per_month": self.goal_days_per_month,
            "reward_points": self.reward_points,
            "reminder_time": self.reminder_time,
            "reminder_enabled": self.reminder_enabled
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Habit":
        """Create habit from dictionary."""
        return cls(
            id=data.get("id"),
            name=data.get("name", ""),
            description=data.get("description", ""),
            category=data.get("category", "Other"),
            color=data.get("color", "#BB8FCE"),
            icon=data.get("icon", "⭐"),
            frequency=data.get("frequency", "daily"),
            streak_count=data.get("streak_count", 0),
            longest_streak=data.get("longest_streak", 0),
            created_date=datetime.fromisoformat(data["created_date"]) if data.get("created_date") else datetime.now(),
            last_completed_date=datetime.fromisoformat(data["last_completed_date"]) if data.get("last_completed_date") else None,
            goal_days_per_week=data.get("goal_days_per_week", 7),
            goal_days_per_month=data.get("goal_days_per_month", 30),
            reward_points=data.get("reward_points", 0),
            reminder_time=data.get("reminder_time"),
            reminder_enabled=data.get("reminder_enabled", False)
        )
