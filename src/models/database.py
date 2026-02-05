"""SQLite database operations for Axilium."""

import sqlite3
import os
from datetime import datetime, date
from typing import List, Optional
from .habit import Habit
from .reward import Reward
from ..utils.constants import DB_PATH, POINTS_PER_COMPLETION


class Database:
    """Manages database operations for Axilium."""
    
    def __init__(self, db_path: str = DB_PATH):
        """Initialize database connection."""
        # Ensure data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
        self._initialize_default_rewards()
    
    def _create_tables(self):
        """Create database tables if they don't exist."""
        cursor = self.conn.cursor()
        
        # Habits table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT NOT NULL,
                color TEXT NOT NULL,
                icon TEXT NOT NULL,
                frequency TEXT NOT NULL,
                streak_count INTEGER DEFAULT 0,
                longest_streak INTEGER DEFAULT 0,
                created_date TEXT NOT NULL,
                last_completed_date TEXT,
                goal_days_per_week INTEGER DEFAULT 7,
                goal_days_per_month INTEGER DEFAULT 30,
                reward_points INTEGER DEFAULT 0,
                reminder_time TEXT,
                reminder_enabled INTEGER DEFAULT 0
            )
        """)
        
        # Completions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                completion_date TEXT NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE
            )
        """)
        
        # Rewards table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rewards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                points_required INTEGER NOT NULL,
                unlocked_date TEXT,
                icon TEXT NOT NULL,
                image_path TEXT
            )
        """)
        
        # Settings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_completions_habit_date ON completions(habit_id, completion_date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_completions_date ON completions(completion_date)")
        
        self.conn.commit()
    
    def _initialize_default_rewards(self):
        """Initialize default rewards if they don't exist."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM rewards")
        if cursor.fetchone()[0] == 0:
            from .reward import DEFAULT_REWARDS
            for reward in DEFAULT_REWARDS:
                cursor.execute("""
                    INSERT INTO rewards (name, description, points_required, unlocked_date, icon, image_path)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    reward.name,
                    reward.description,
                    reward.points_required,
                    reward.unlocked_date.isoformat() if reward.unlocked_date else None,
                    reward.icon,
                    reward.image_path
                ))
            self.conn.commit()
    
    # Habit operations
    def add_habit(self, habit: Habit) -> int:
        """Add a new habit and return its ID."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO habits (name, description, category, color, icon, frequency,
                              streak_count, longest_streak, created_date, last_completed_date,
                              goal_days_per_week, goal_days_per_month, reward_points,
                              reminder_time, reminder_enabled)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            habit.name, habit.description, habit.category, habit.color, habit.icon,
            habit.frequency, habit.streak_count, habit.longest_streak,
            habit.created_date.isoformat(),
            habit.last_completed_date.isoformat() if habit.last_completed_date else None,
            habit.goal_days_per_week, habit.goal_days_per_month, habit.reward_points,
            habit.reminder_time, 1 if habit.reminder_enabled else 0
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_habit(self, habit_id: int) -> Optional[Habit]:
        """Get a habit by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM habits WHERE id = ?", (habit_id,))
        row = cursor.fetchone()
        if row:
            return self._row_to_habit(row)
        return None
    
    def get_all_habits(self) -> List[Habit]:
        """Get all habits."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM habits ORDER BY created_date DESC")
        return [self._row_to_habit(row) for row in cursor.fetchall()]
    
    def update_habit(self, habit: Habit):
        """Update an existing habit."""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE habits SET name = ?, description = ?, category = ?, color = ?, icon = ?,
                            frequency = ?, streak_count = ?, longest_streak = ?,
                            last_completed_date = ?, goal_days_per_week = ?,
                            goal_days_per_month = ?, reward_points = ?, reminder_time = ?,
                            reminder_enabled = ?
            WHERE id = ?
        """, (
            habit.name, habit.description, habit.category, habit.color, habit.icon,
            habit.frequency, habit.streak_count, habit.longest_streak,
            habit.last_completed_date.isoformat() if habit.last_completed_date else None,
            habit.goal_days_per_week, habit.goal_days_per_month, habit.reward_points,
            habit.reminder_time, 1 if habit.reminder_enabled else 0, habit.id
        ))
        self.conn.commit()
    
    def delete_habit(self, habit_id: int):
        """Delete a habit and its completions."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        self.conn.commit()
    
    def _row_to_habit(self, row) -> Habit:
        """Convert database row to Habit object."""
        return Habit(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            category=row["category"],
            color=row["color"],
            icon=row["icon"],
            frequency=row["frequency"],
            streak_count=row["streak_count"],
            longest_streak=row["longest_streak"],
            created_date=datetime.fromisoformat(row["created_date"]),
            last_completed_date=datetime.fromisoformat(row["last_completed_date"]) if row["last_completed_date"] else None,
            goal_days_per_week=row["goal_days_per_week"],
            goal_days_per_month=row["goal_days_per_month"],
            reward_points=row["reward_points"],
            reminder_time=row["reminder_time"],
            reminder_enabled=bool(row["reminder_enabled"])
        )
    
    # Completion operations
    def add_completion(self, habit_id: int, completion_date: date = None) -> bool:
        """Add a completion record. Returns True if streak was updated."""
        if completion_date is None:
            completion_date = date.today()
        
        cursor = self.conn.cursor()
        
        # Check if already completed today
        cursor.execute("""
            SELECT COUNT(*) FROM completions
            WHERE habit_id = ? AND completion_date = ?
        """, (habit_id, completion_date.isoformat()))
        
        if cursor.fetchone()[0] > 0:
            return False  # Already completed
        
        # Add completion
        cursor.execute("""
            INSERT INTO completions (habit_id, completion_date)
            VALUES (?, ?)
        """, (habit_id, completion_date.isoformat()))
        
        # Update habit streak and points
        habit = self.get_habit(habit_id)
        if habit:
            # Check if this continues the streak
            yesterday = date.fromordinal(completion_date.toordinal() - 1)
            cursor.execute("""
                SELECT COUNT(*) FROM completions
                WHERE habit_id = ? AND completion_date = ?
            """, (habit_id, yesterday.isoformat()))
            
            if cursor.fetchone()[0] > 0 or habit.last_completed_date is None:
                # Continue streak
                habit.streak_count += 1
            else:
                # New streak
                habit.streak_count = 1
            
            if habit.streak_count > habit.longest_streak:
                habit.longest_streak = habit.streak_count
            
            habit.last_completed_date = datetime.combine(completion_date, datetime.min.time())
            habit.reward_points += POINTS_PER_COMPLETION
            
            self.update_habit(habit)
            self.conn.commit()
            return True
        
        return False
    
    def get_completions(self, habit_id: int, start_date: date = None, end_date: date = None) -> List[date]:
        """Get completion dates for a habit."""
        cursor = self.conn.cursor()
        
        if start_date and end_date:
            cursor.execute("""
                SELECT completion_date FROM completions
                WHERE habit_id = ? AND completion_date BETWEEN ? AND ?
                ORDER BY completion_date
            """, (habit_id, start_date.isoformat(), end_date.isoformat()))
        else:
            cursor.execute("""
                SELECT completion_date FROM completions
                WHERE habit_id = ?
                ORDER BY completion_date
            """, (habit_id,))
        
        return [date.fromisoformat(row[0]) for row in cursor.fetchall()]
    
    def get_completion_count(self, habit_id: int, start_date: date = None, end_date: date = None) -> int:
        """Get completion count for a habit in a date range."""
        cursor = self.conn.cursor()
        
        if start_date and end_date:
            cursor.execute("""
                SELECT COUNT(*) FROM completions
                WHERE habit_id = ? AND completion_date BETWEEN ? AND ?
            """, (habit_id, start_date.isoformat(), end_date.isoformat()))
        else:
            cursor.execute("""
                SELECT COUNT(*) FROM completions
                WHERE habit_id = ?
            """, (habit_id,))
        
        return cursor.fetchone()[0]
    
    # Reward operations
    def get_all_rewards(self) -> List[Reward]:
        """Get all rewards."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM rewards ORDER BY points_required")
        return [self._row_to_reward(row) for row in cursor.fetchall()]
    
    def unlock_reward(self, reward_id: int):
        """Unlock a reward."""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE rewards SET unlocked_date = ?
            WHERE id = ?
        """, (datetime.now().isoformat(), reward_id))
        self.conn.commit()
    
    def get_total_points(self) -> int:
        """Get total reward points across all habits."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT SUM(reward_points) FROM habits")
        result = cursor.fetchone()[0]
        return result if result else 0
    
    def _row_to_reward(self, row) -> Reward:
        """Convert database row to Reward object."""
        return Reward(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            points_required=row["points_required"],
            unlocked_date=datetime.fromisoformat(row["unlocked_date"]) if row["unlocked_date"] else None,
            icon=row["icon"],
            image_path=row["image_path"]
        )
    
    # Settings operations
    def get_setting(self, key: str, default: str = None) -> Optional[str]:
        """Get a setting value."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row[0] if row else default
    
    def set_setting(self, key: str, value: str):
        """Set a setting value."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO settings (key, value)
            VALUES (?, ?)
        """, (key, value))
        self.conn.commit()
    
    def close(self):
        """Close database connection."""
        self.conn.close()
