"""Reward system model."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Reward:
    """Represents an unlocked reward."""
    
    id: Optional[int]
    name: str
    description: str
    points_required: int
    unlocked_date: Optional[datetime]
    icon: str
    image_path: Optional[str]
    
    def __post_init__(self):
        """Initialize default values."""
        if self.id is None:
            self.id = 0
    
    def is_unlocked(self) -> bool:
        """Check if reward is unlocked."""
        return self.unlocked_date is not None
    
    def to_dict(self) -> dict:
        """Convert reward to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "points_required": self.points_required,
            "unlocked_date": self.unlocked_date.isoformat() if self.unlocked_date else None,
            "icon": self.icon,
            "image_path": self.image_path
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Reward":
        """Create reward from dictionary."""
        return cls(
            id=data.get("id"),
            name=data.get("name", ""),
            description=data.get("description", ""),
            points_required=data.get("points_required", 0),
            unlocked_date=datetime.fromisoformat(data["unlocked_date"]) if data.get("unlocked_date") else None,
            icon=data.get("icon", "🎁"),
            image_path=data.get("image_path")
        )


# Default rewards
DEFAULT_REWARDS = [
    Reward(0, "First Steps", "Complete your first habit!", 50, None, "🌱", None),
    Reward(1, "Getting Started", "Reach 100 points", 100, None, "⭐", None),
    Reward(2, "On a Roll", "Reach 250 points", 250, None, "🔥", None),
    Reward(3, "Halfway Hero", "Reach 500 points", 500, None, "💪", None),
    Reward(4, "Champion", "Reach 1000 points", 1000, None, "🏆", None),
    Reward(5, "Master", "Reach 2500 points", 2500, None, "👑", None),
    Reward(6, "Legend", "Reach 5000 points", 5000, None, "🌟", None),
]
