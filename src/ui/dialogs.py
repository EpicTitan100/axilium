"""Dialog windows for Axilium."""

import customtkinter as ctk
from typing import Optional, Callable
from ..models.habit import Habit
from ..utils.constants import CATEGORIES, FREQUENCIES, CATEGORY_COLORS


class HabitDialog(ctk.CTkToplevel):
    """Dialog for adding/editing habits."""
    
    def __init__(self, parent, habit: Optional[Habit] = None, on_save: Optional[Callable] = None):
        """Initialize habit dialog."""
        super().__init__(parent)
        
        self.habit = habit
        self.on_save = on_save
        self.result = None
        
        self.title("Add Habit" if habit is None else "Edit Habit")
        self.geometry("500x600")
        self.resizable(False, False)
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        
        # Center dialog
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
    
    def _create_widgets(self):
        """Create dialog widgets."""
        # Main frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Name
        ctk.CTkLabel(main_frame, text="Habit Name:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 5))
        self.name_entry = ctk.CTkEntry(main_frame, width=400, height=35)
        self.name_entry.pack(fill="x", pady=(0, 15))
        
        # Description
        ctk.CTkLabel(main_frame, text="Description:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 5))
        self.description_text = ctk.CTkTextbox(main_frame, width=400, height=80)
        self.description_text.pack(fill="x", pady=(0, 15))
        
        # Category
        ctk.CTkLabel(main_frame, text="Category:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 5))
        self.category_var = ctk.StringVar(value=CATEGORIES[0])
        self.category_menu = ctk.CTkOptionMenu(
            main_frame,
            values=CATEGORIES,
            variable=self.category_var,
            width=400,
            height=35,
            command=self._on_category_change
        )
        self.category_menu.pack(fill="x", pady=(0, 15))
        
        # Color preview
        self.color_frame = ctk.CTkFrame(main_frame, width=400, height=40)
        self.color_frame.pack(fill="x", pady=(0, 15))
        self.color_label = ctk.CTkLabel(self.color_frame, text="", width=380, height=30)
        self.color_label.pack(pady=5)
        
        # Frequency
        ctk.CTkLabel(main_frame, text="Frequency:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 5))
        self.frequency_var = ctk.StringVar(value=FREQUENCIES[0])
        self.frequency_menu = ctk.CTkOptionMenu(
            main_frame,
            values=FREQUENCIES,
            variable=self.frequency_var,
            width=400,
            height=35
        )
        self.frequency_menu.pack(fill="x", pady=(0, 15))
        
        # Icon
        ctk.CTkLabel(main_frame, text="Icon (emoji):", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 5))
        self.icon_entry = ctk.CTkEntry(main_frame, width=400, height=35)
        self.icon_entry.pack(fill="x", pady=(0, 15))
        
        # Goals
        goals_frame = ctk.CTkFrame(main_frame)
        goals_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(goals_frame, text="Goal (days per week):", font=ctk.CTkFont(size=12)).pack(side="left", padx=10)
        self.goal_week_var = ctk.StringVar(value="7")
        self.goal_week_entry = ctk.CTkEntry(goals_frame, width=80, textvariable=self.goal_week_var)
        self.goal_week_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(goals_frame, text="Goal (days per month):", font=ctk.CTkFont(size=12)).pack(side="left", padx=10)
        self.goal_month_var = ctk.StringVar(value="30")
        self.goal_month_entry = ctk.CTkEntry(goals_frame, width=80, textvariable=self.goal_month_var)
        self.goal_month_entry.pack(side="left", padx=5)
        
        # Reminder
        reminder_frame = ctk.CTkFrame(main_frame)
        reminder_frame.pack(fill="x", pady=(0, 15))
        
        self.reminder_enabled_var = ctk.BooleanVar(value=False)
        reminder_check = ctk.CTkCheckBox(
            reminder_frame,
            text="Enable Reminder",
            variable=self.reminder_enabled_var
        )
        reminder_check.pack(side="left", padx=10)
        
        ctk.CTkLabel(reminder_frame, text="Time (HH:MM):", font=ctk.CTkFont(size=12)).pack(side="left", padx=10)
        self.reminder_time_entry = ctk.CTkEntry(reminder_frame, width=100, placeholder_text="09:00")
        self.reminder_time_entry.pack(side="left", padx=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self._on_cancel,
            width=150,
            height=35,
            fg_color="gray"
        ).pack(side="right", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Save",
            command=self._on_save,
            width=150,
            height=35
        ).pack(side="right", padx=5)
        
        # Load existing habit data
        if self.habit:
            self._load_habit_data()
        
        # Update color preview
        self._on_category_change(self.category_var.get())
    
    def _on_category_change(self, category: str):
        """Update color preview when category changes."""
        color = CATEGORY_COLORS.get(category, "#BB8FCE")
        self.color_label.configure(text=f"Color: {category}", fg_color=color)
    
    def _load_habit_data(self):
        """Load existing habit data into form."""
        if not self.habit:
            return
        
        self.name_entry.insert(0, self.habit.name)
        self.description_text.insert("1.0", self.habit.description)
        self.category_var.set(self.habit.category)
        self.frequency_var.set(self.habit.frequency)
        self.icon_entry.insert(0, self.habit.icon)
        self.goal_week_var.set(str(self.habit.goal_days_per_week))
        self.goal_month_var.set(str(self.habit.goal_days_per_month))
        self.reminder_enabled_var.set(self.habit.reminder_enabled)
        if self.habit.reminder_time:
            self.reminder_time_entry.insert(0, self.habit.reminder_time)
        
        self._on_category_change(self.habit.category)
    
    def _on_save(self):
        """Handle save button click."""
        name = self.name_entry.get().strip()
        if not name:
            return
        
        description = self.description_text.get("1.0", "end-1c").strip()
        category = self.category_var.get()
        frequency = self.frequency_var.get()
        icon = self.icon_entry.get().strip() or "⭐"
        color = CATEGORY_COLORS.get(category, "#BB8FCE")
        
        try:
            goal_week = int(self.goal_week_var.get())
            goal_month = int(self.goal_month_var.get())
        except ValueError:
            goal_week = 7
            goal_month = 30
        
        reminder_enabled = self.reminder_enabled_var.get()
        reminder_time = self.reminder_time_entry.get().strip() if reminder_enabled else None
        
        if self.habit:
            # Update existing habit
            self.habit.name = name
            self.habit.description = description
            self.habit.category = category
            self.habit.color = color
            self.habit.frequency = frequency
            self.habit.icon = icon
            self.habit.goal_days_per_week = goal_week
            self.habit.goal_days_per_month = goal_month
            self.habit.reminder_enabled = reminder_enabled
            self.habit.reminder_time = reminder_time
            self.result = self.habit
        else:
            # Create new habit
            from datetime import datetime
            from ..models.habit import Habit
            
            self.result = Habit(
                id=None,
                name=name,
                description=description,
                category=category,
                color=color,
                icon=icon,
                frequency=frequency,
                streak_count=0,
                longest_streak=0,
                created_date=datetime.now(),
                last_completed_date=None,
                goal_days_per_week=goal_week,
                goal_days_per_month=goal_month,
                reward_points=0,
                reminder_time=reminder_time,
                reminder_enabled=reminder_enabled
            )
        
        if self.on_save:
            self.on_save(self.result)
        
        self.destroy()
    
    def _on_cancel(self):
        """Handle cancel button click."""
        self.result = None
        self.destroy()
