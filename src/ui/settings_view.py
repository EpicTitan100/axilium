"""Settings view for Axilium."""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from ..models.database import Database
from ..services.export_service import ExportService
from ..utils.themes import THEMES, DEFAULT_THEME


class SettingsView(ctk.CTkScrollableFrame):
    """Settings and configuration view."""
    
    def __init__(self, parent, db: Database, on_theme_change: callable = None):
        """Initialize settings view."""
        super().__init__(parent)
        
        self.db = db
        self.export_service = ExportService(db)
        self.on_theme_change = on_theme_change
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create settings widgets."""
        # Title
        title = ctk.CTkLabel(
            self,
            text="⚙️ Settings",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=(20, 30))
        
        # Theme selection
        self._create_theme_section()
        
        # Data management
        self._create_data_section()
        
        # About section
        self._create_about_section()
    
    def _create_theme_section(self):
        """Create theme selection section."""
        theme_frame = ctk.CTkFrame(self)
        theme_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            theme_frame,
            text="Theme",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 10))
        
        current_theme = self.db.get_setting("theme", DEFAULT_THEME)
        self.theme_var = ctk.StringVar(value=current_theme)
        
        theme_options = list(THEMES.keys())
        theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=theme_options,
            variable=self.theme_var,
            command=self._on_theme_change,
            width=300
        )
        theme_menu.pack(anchor="w", padx=20, pady=(0, 20))
    
    def _create_data_section(self):
        """Create data management section."""
        data_frame = ctk.CTkFrame(self)
        data_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            data_frame,
            text="Data Management",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 10))
        
        # Export buttons
        export_frame = ctk.CTkFrame(data_frame, fg_color="transparent")
        export_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(
            export_frame,
            text="Export to JSON",
            command=self._export_json,
            width=150,
            height=35
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            export_frame,
            text="Export to CSV",
            command=self._export_csv,
            width=150,
            height=35
        ).pack(side="left", padx=5)
        
        # Import button
        import_frame = ctk.CTkFrame(data_frame, fg_color="transparent")
        import_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(
            import_frame,
            text="Import from JSON",
            command=self._import_json,
            width=150,
            height=35,
            fg_color="gray"
        ).pack(side="left", padx=5)
        
        # Reset button
        reset_frame = ctk.CTkFrame(data_frame, fg_color="transparent")
        reset_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        ctk.CTkButton(
            reset_frame,
            text="Reset All Data",
            command=self._reset_data,
            width=150,
            height=35,
            fg_color="#FF6B6B",
            hover_color="#FF5252"
        ).pack(side="left", padx=5)
    
    def _create_about_section(self):
        """Create about section."""
        about_frame = ctk.CTkFrame(self)
        about_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            about_frame,
            text="About",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 10))
        
        about_text = """
Axilium Habit Tracker v1.0.0

A fun and engaging habit tracking application
built with Python and CustomTkinter.

Track your habits, build streaks, earn rewards,
and achieve your goals!
        """
        
        ctk.CTkLabel(
            about_frame,
            text=about_text.strip(),
            font=ctk.CTkFont(size=12),
            justify="left"
        ).pack(anchor="w", padx=20, pady=(0, 20))
    
    def _on_theme_change(self, theme_name: str):
        """Handle theme change."""
        self.db.set_setting("theme", theme_name)
        if self.on_theme_change:
            self.on_theme_change(theme_name)
    
    def _export_json(self):
        """Export data to JSON."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.export_service.export_to_json(file_path)
                messagebox.showinfo("Success", "Data exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data: {e}")
    
    def _export_csv(self):
        """Export data to CSV."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.export_service.export_to_csv(file_path)
                messagebox.showinfo("Success", "Data exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data: {e}")
    
    def _import_json(self):
        """Import data from JSON."""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            result = messagebox.askyesno(
                "Confirm Import",
                "This will merge imported data with existing data. Continue?"
            )
            if result:
                try:
                    success = self.export_service.import_from_json(file_path)
                    if success:
                        messagebox.showinfo("Success", "Data imported successfully!")
                    else:
                        messagebox.showerror("Error", "Failed to import data.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to import data: {e}")
    
    def _reset_data(self):
        """Reset all data."""
        result = messagebox.askyesno(
            "Confirm Reset",
            "Are you sure you want to delete all habits and data? This cannot be undone!",
            icon="warning"
        )
        if result:
            # Delete all habits (completions will cascade)
            habits = self.db.get_all_habits()
            for habit in habits:
                self.db.delete_habit(habit.id)
            
            # Reset rewards
            rewards = self.db.get_all_rewards()
            for reward in rewards:
                if reward.unlocked_date:
                    cursor = self.db.conn.cursor()
                    cursor.execute("UPDATE rewards SET unlocked_date = NULL WHERE id = ?", (reward.id,))
                    self.db.conn.commit()
            
            messagebox.showinfo("Success", "All data has been reset.")
