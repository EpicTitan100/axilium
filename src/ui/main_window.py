"""Main application window for Axilium."""

import customtkinter as ctk
from typing import Optional
from plyer import notification
from ..models.database import Database
from ..models.habit import Habit
from ..models.reward import Reward
from ..services.reminder_service import ReminderService
from ..services.stats_service import StatsService
from ..utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT, POINTS_PER_COMPLETION, REWARD_MILESTONES
from ..utils.themes import get_theme
from .habit_card import HabitCard
from .stats_view import StatsView
from .settings_view import SettingsView
from .dialogs import HabitDialog


class MainWindow(ctk.CTk):
    """Main application window."""
    
    def __init__(self):
        """Initialize main window."""
        super().__init__()
        
        # Initialize database
        self.db = Database()
        
        # Initialize services
        self.reminder_service = ReminderService(self.db, self._show_notification)
        self.stats_service = StatsService(self.db)
        
        # Setup window
        self.title("Axilium - Habit Tracker")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        
        # Apply theme
        self._apply_theme()
        
        # Create UI
        self._create_widgets()
        
        # Load habits
        self._refresh_habits()
        
        # Check for unlocked rewards
        self._check_rewards()
        
        # Start reminder service
        self.reminder_service.start()
        
        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _apply_theme(self):
        """Apply current theme."""
        theme_name = self.db.get_setting("theme", "dark")
        theme = get_theme(theme_name)
        
        ctk.set_appearance_mode("dark" if theme_name != "light" else "light")
        ctk.set_default_color_theme("blue")
        
        # Store theme for custom colors
        self.current_theme = theme
    
    def _create_widgets(self):
        """Create main window widgets."""
        # Main container
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self._create_sidebar()
        
        # Main content area
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # Show habits view by default
        self._show_habits_view()
    
    def _create_sidebar(self):
        """Create navigation sidebar."""
        sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(4, weight=1)
        
        # Logo/Title
        title_label = ctk.CTkLabel(
            sidebar,
            text="⚡ Axilium",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Navigation buttons
        self.nav_habits_btn = ctk.CTkButton(
            sidebar,
            text="📋 Habits",
            command=self._show_habits_view,
            width=180,
            height=40,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            anchor="w"
        )
        self.nav_habits_btn.pack(pady=5, padx=10)
        
        self.nav_stats_btn = ctk.CTkButton(
            sidebar,
            text="📊 Statistics",
            command=self._show_stats_view,
            width=180,
            height=40,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            anchor="w"
        )
        self.nav_stats_btn.pack(pady=5, padx=10)
        
        self.nav_rewards_btn = ctk.CTkButton(
            sidebar,
            text="🎁 Rewards",
            command=self._show_rewards_view,
            width=180,
            height=40,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            anchor="w"
        )
        self.nav_rewards_btn.pack(pady=5, padx=10)
        
        self.nav_settings_btn = ctk.CTkButton(
            sidebar,
            text="⚙️ Settings",
            command=self._show_settings_view,
            width=180,
            height=40,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            anchor="w"
        )
        self.nav_settings_btn.pack(pady=5, padx=10)
        
        # Quick stats
        self.quick_stats_frame = ctk.CTkFrame(sidebar)
        self.quick_stats_frame.pack(fill="x", padx=10, pady=20, side="bottom")
        
        self._update_quick_stats()
    
    def _update_quick_stats(self):
        """Update quick stats in sidebar."""
        for widget in self.quick_stats_frame.winfo_children():
            widget.destroy()
        
        habits = self.db.get_all_habits()
        total_points = self.db.get_total_points()
        completion_rate = self.stats_service.get_overall_completion_rate(30)
        
        ctk.CTkLabel(
            self.quick_stats_frame,
            text="Quick Stats",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5))
        
        ctk.CTkLabel(
            self.quick_stats_frame,
            text=f"Habits: {len(habits)}",
            font=ctk.CTkFont(size=12)
        ).pack()
        
        ctk.CTkLabel(
            self.quick_stats_frame,
            text=f"Points: {total_points}",
            font=ctk.CTkFont(size=12)
        ).pack()
        
        ctk.CTkLabel(
            self.quick_stats_frame,
            text=f"Rate: {completion_rate:.1f}%",
            font=ctk.CTkFont(size=12)
        ).pack(pady=(0, 10))
    
    def _show_habits_view(self):
        """Show habits view."""
        self._clear_content()
        self._highlight_nav_button(self.nav_habits_btn)
        
        # Header
        header_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        title = ctk.CTkLabel(
            header_frame,
            text="📋 My Habits",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(side="left")
        
        add_btn = ctk.CTkButton(
            header_frame,
            text="+ Add Habit",
            command=self._add_habit,
            width=120,
            height=35
        )
        add_btn.pack(side="right")
        
        # Habits container
        self.habits_container = ctk.CTkScrollableFrame(self.content_frame)
        self.habits_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self._refresh_habits()
    
    def _show_stats_view(self):
        """Show statistics view."""
        self._clear_content()
        self._highlight_nav_button(self.nav_stats_btn)
        
        stats_view = StatsView(self.content_frame, self.db)
        stats_view.pack(fill="both", expand=True)
    
    def _show_rewards_view(self):
        """Show rewards view."""
        self._clear_content()
        self._highlight_nav_button(self.nav_rewards_btn)
        
        # Header
        header_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        title = ctk.CTkLabel(
            header_frame,
            text="🎁 Rewards",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(side="left")
        
        total_points = self.db.get_total_points()
        points_label = ctk.CTkLabel(
            header_frame,
            text=f"Total Points: {total_points}",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        points_label.pack(side="right", padx=20)
        
        # Rewards grid
        rewards_container = ctk.CTkScrollableFrame(self.content_frame)
        rewards_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        rewards = self.db.get_all_rewards()
        for reward in rewards:
            self._create_reward_card(rewards_container, reward)
    
    def _show_settings_view(self):
        """Show settings view."""
        self._clear_content()
        self._highlight_nav_button(self.nav_settings_btn)
        
        settings_view = SettingsView(
            self.content_frame,
            self.db,
            on_theme_change=self._on_theme_change
        )
        settings_view.pack(fill="both", expand=True)
    
    def _create_reward_card(self, parent, reward: Reward):
        """Create a reward card."""
        unlocked = reward.is_unlocked()
        
        card = ctk.CTkFrame(
            parent,
            corner_radius=15,
            fg_color=("gray85", "gray25") if unlocked else ("gray95", "gray15")
        )
        card.pack(fill="x", padx=10, pady=10)
        
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=15)
        
        # Icon and name
        icon_label = ctk.CTkLabel(
            content_frame,
            text=reward.icon,
            font=ctk.CTkFont(size=40)
        )
        icon_label.pack(side="left", padx=(0, 15))
        
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)
        
        name_label = ctk.CTkLabel(
            info_frame,
            text=reward.name,
            font=ctk.CTkFont(size=18, weight="bold")
        )
        name_label.pack(anchor="w")
        
        desc_label = ctk.CTkLabel(
            info_frame,
            text=reward.description,
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        desc_label.pack(anchor="w")
        
        # Points and status
        status_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        status_frame.pack(side="right")
        
        points_label = ctk.CTkLabel(
            status_frame,
            text=f"{reward.points_required} pts",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        points_label.pack()
        
        if unlocked:
            status_label = ctk.CTkLabel(
                status_frame,
                text="✓ Unlocked",
                font=ctk.CTkFont(size=12),
                text_color="#4ECDC4"
            )
            status_label.pack()
        else:
            total_points = self.db.get_total_points()
            remaining = reward.points_required - total_points
            if remaining > 0:
                status_label = ctk.CTkLabel(
                    status_frame,
                    text=f"{remaining} pts to go",
                    font=ctk.CTkFont(size=12),
                    text_color="gray"
                )
                status_label.pack()
    
    def _highlight_nav_button(self, button):
        """Highlight the active navigation button."""
        for btn in [self.nav_habits_btn, self.nav_stats_btn, self.nav_rewards_btn, self.nav_settings_btn]:
            btn.configure(fg_color="transparent")
        button.configure(fg_color=("gray75", "gray25"))
    
    def _clear_content(self):
        """Clear content area."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def _refresh_habits(self):
        """Refresh habits display."""
        if hasattr(self, 'habits_container'):
            for widget in self.habits_container.winfo_children():
                widget.destroy()
            
            habits = self.db.get_all_habits()
            
            if not habits:
                empty_label = ctk.CTkLabel(
                    self.habits_container,
                    text="No habits yet!\nClick 'Add Habit' to get started.",
                    font=ctk.CTkFont(size=16),
                    text_color="gray"
                )
                empty_label.pack(pady=50)
            else:
                # Create grid layout
                for i, habit in enumerate(habits):
                    card = HabitCard(
                        self.habits_container,
                        habit,
                        self.db,
                        on_complete=self._on_habit_complete,
                        on_edit=self._edit_habit,
                        on_delete=self._delete_habit
                    )
                    card.pack(fill="x", padx=10, pady=10)
            
            self._update_quick_stats()
    
    def _add_habit(self):
        """Show add habit dialog."""
        dialog = HabitDialog(self, on_save=self._save_habit)
        self.wait_window(dialog)
    
    def _edit_habit(self, habit: Habit):
        """Show edit habit dialog."""
        dialog = HabitDialog(self, habit=habit, on_save=self._save_habit)
        self.wait_window(dialog)
    
    def _save_habit(self, habit: Habit):
        """Save habit (add or update)."""
        if habit.id and habit.id > 0:
            self.db.update_habit(habit)
            self.reminder_service.update_reminders()
        else:
            habit_id = self.db.add_habit(habit)
            habit.id = habit_id
            self.reminder_service.update_reminders()
        
        self._refresh_habits()
    
    def _delete_habit(self, habit: Habit):
        """Delete a habit."""
        import tkinter.messagebox as messagebox
        result = messagebox.askyesno(
            "Delete Habit",
            f"Are you sure you want to delete '{habit.name}'?",
            icon="warning"
        )
        if result:
            self.db.delete_habit(habit.id)
            self._refresh_habits()
    
    def _on_habit_complete(self, habit: Habit):
        """Handle habit completion."""
        self._refresh_habits()
        self._check_rewards()
        self._update_quick_stats()
    
    def _check_rewards(self):
        """Check and unlock rewards based on points."""
        total_points = self.db.get_total_points()
        rewards = self.db.get_all_rewards()
        
        for reward in rewards:
            if not reward.is_unlocked() and total_points >= reward.points_required:
                self.db.unlock_reward(reward.id)
                self._show_reward_notification(reward)
    
    def _show_reward_notification(self, reward: Reward):
        """Show notification when reward is unlocked."""
        try:
            notification.notify(
                title="🎉 Reward Unlocked!",
                message=f"You unlocked: {reward.name}!\n{reward.description}",
                timeout=5
            )
        except:
            pass  # Notification might not work on all systems
    
    def _show_notification(self, title: str, message: str):
        """Show reminder notification."""
        try:
            notification.notify(
                title=title,
                message=message,
                timeout=5
            )
        except:
            pass
    
    def _on_theme_change(self, theme_name: str):
        """Handle theme change."""
        self._apply_theme()
        # Show message that app restart is needed for full theme change
        import tkinter.messagebox as messagebox
        messagebox.showinfo(
            "Theme Changed",
            "Theme has been saved. Some changes will take effect after restarting the application."
        )
    
    def _on_closing(self):
        """Handle window closing."""
        self.reminder_service.stop()
        self.db.close()
        self.destroy()
