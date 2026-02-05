"""Habit card component for displaying habits."""

import customtkinter as ctk
from datetime import date, timedelta
from typing import Callable, Optional
from ..models.habit import Habit
from ..models.database import Database


class HabitCard(ctk.CTkFrame):
    """Card component for displaying a habit."""
    
    def __init__(
        self,
        parent,
        habit: Habit,
        db: Database,
        on_complete: Optional[Callable] = None,
        on_edit: Optional[Callable] = None,
        on_delete: Optional[Callable] = None
    ):
        """Initialize habit card."""
        super().__init__(parent, corner_radius=15, fg_color=("gray90", "gray20"))
        
        self.habit = habit
        self.db = db
        self.on_complete = on_complete
        self.on_edit = on_edit
        self.on_delete = on_delete
        
        self._create_widgets()
        self._update_progress()
    
    def _create_widgets(self):
        """Create card widgets."""
        # Main container with padding
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Header with icon and name
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Icon
        icon_label = ctk.CTkLabel(
            header_frame,
            text=self.habit.icon,
            font=ctk.CTkFont(size=32),
            width=50
        )
        icon_label.pack(side="left", padx=(0, 10))
        
        # Name and category
        info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)
        
        name_label = ctk.CTkLabel(
            info_frame,
            text=self.habit.name,
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        name_label.pack(fill="x")
        
        category_label = ctk.CTkLabel(
            info_frame,
            text=self.habit.category,
            font=ctk.CTkFont(size=12),
            anchor="w",
            text_color="gray"
        )
        category_label.pack(fill="x")
        
        # Streak display
        streak_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        streak_frame.pack(fill="x", pady=(0, 10))
        
        streak_text = f"🔥 {self.habit.streak_count} day streak"
        if self.habit.longest_streak > self.habit.streak_count:
            streak_text += f" (Best: {self.habit.longest_streak})"
        
        streak_label = ctk.CTkLabel(
            streak_frame,
            text=streak_text,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.habit.color
        )
        streak_label.pack(side="left")
        
        # Progress bar
        self.progress_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=ctk.CTkFont(size=11),
            anchor="w"
        )
        self.progress_label.pack(fill="x", pady=(0, 5))
        
        self.progress_bar = ctk.CTkProgressBar(main_frame, height=20)
        self.progress_bar.pack(fill="x", pady=(0, 10))
        self.progress_bar.set(0)
        
        # Action buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x")
        
        # Complete button
        complete_btn = ctk.CTkButton(
            button_frame,
            text="✓ Complete",
            command=self._on_complete,
            width=120,
            height=35,
            fg_color=self.habit.color,
            hover_color=self._darken_color(self.habit.color)
        )
        complete_btn.pack(side="left", padx=(0, 5))
        
        # Edit button
        edit_btn = ctk.CTkButton(
            button_frame,
            text="✎ Edit",
            command=self._on_edit,
            width=80,
            height=35,
            fg_color="gray"
        )
        edit_btn.pack(side="left", padx=5)
        
        # Delete button
        delete_btn = ctk.CTkButton(
            button_frame,
            text="✕ Delete",
            command=self._on_delete,
            width=80,
            height=35,
            fg_color="#FF6B6B",
            hover_color="#FF5252"
        )
        delete_btn.pack(side="left", padx=5)
    
    def _darken_color(self, color: str) -> str:
        """Darken a hex color."""
        # Simple darkening - convert hex to RGB, reduce brightness
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        r = max(0, int(r * 0.8))
        g = max(0, int(g * 0.8))
        b = max(0, int(b * 0.8))
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _update_progress(self):
        """Update progress bar based on current period."""
        today = date.today()
        
        if self.habit.frequency == "daily":
            # Weekly progress
            week_start = today - timedelta(days=today.weekday())
            completed = self.db.get_completion_count(self.habit.id, week_start, today)
            total = self.habit.goal_days_per_week
            period = "week"
        else:
            # Monthly progress
            month_start = date(today.year, today.month, 1)
            completed = self.db.get_completion_count(self.habit.id, month_start, today)
            total = self.habit.goal_days_per_month
            period = "month"
        
        progress = min(completed / total, 1.0) if total > 0 else 0.0
        self.progress_bar.set(progress)
        self.progress_label.configure(
            text=f"{completed}/{total} days completed this {period} ({int(progress * 100)}%)"
        )
    
    def _on_complete(self):
        """Handle complete button click."""
        success = self.db.add_completion(self.habit.id)
        if success:
            # Update habit data
            self.habit = self.db.get_habit(self.habit.id)
            if self.habit:
                self._update_progress()
                # Update streak display
                for widget in self.winfo_children():
                    widget.destroy()
                self._create_widgets()
                
                if self.on_complete:
                    self.on_complete(self.habit)
    
    def _on_edit(self):
        """Handle edit button click."""
        if self.on_edit:
            self.on_edit(self.habit)
    
    def _on_delete(self):
        """Handle delete button click."""
        if self.on_delete:
            self.on_delete(self.habit)
    
    def update_display(self):
        """Refresh the card display."""
        self.habit = self.db.get_habit(self.habit.id)
        if self.habit:
            for widget in self.winfo_children():
                widget.destroy()
            self._create_widgets()
