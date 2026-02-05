"""Statistics view for Axilium."""

import customtkinter as ctk
from datetime import date, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from ..services.stats_service import StatsService
from ..models.database import Database


class StatsView(ctk.CTkScrollableFrame):
    """Statistics and visualization view."""
    
    def __init__(self, parent, db: Database):
        """Initialize stats view."""
        super().__init__(parent)
        
        self.db = db
        self.stats_service = StatsService(db)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create stats view widgets."""
        # Title
        title = ctk.CTkLabel(
            self,
            text="📊 Statistics",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=(20, 30))
        
        # Summary cards
        self._create_summary_cards()
        
        # Charts
        self._create_charts()
    
    def _create_summary_cards(self):
        """Create summary statistic cards."""
        summary_frame = ctk.CTkFrame(self, fg_color="transparent")
        summary_frame.pack(fill="x", padx=20, pady=10)
        
        # Overall completion rate
        completion_rate = self.stats_service.get_overall_completion_rate(30)
        self._create_stat_card(
            summary_frame,
            "Completion Rate",
            f"{completion_rate:.1f}%",
            "Last 30 days"
        )
        
        # Average streak
        avg_streak = self.stats_service.get_average_streak()
        self._create_stat_card(
            summary_frame,
            "Average Streak",
            f"{avg_streak:.1f} days",
            "Across all habits"
        )
        
        # Total habits
        habits = self.db.get_all_habits()
        self._create_stat_card(
            summary_frame,
            "Total Habits",
            str(len(habits)),
            "Active habits"
        )
        
        # Total points
        total_points = self.db.get_total_points()
        self._create_stat_card(
            summary_frame,
            "Total Points",
            str(total_points),
            "Reward points earned"
        )
    
    def _create_stat_card(self, parent, title: str, value: str, subtitle: str):
        """Create a statistic card."""
        card = ctk.CTkFrame(parent, corner_radius=10, width=200, height=120)
        card.pack(side="left", padx=10, fill="both", expand=True)
        
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        title_label.pack(pady=(15, 5))
        
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=32, weight="bold")
        )
        value_label.pack()
        
        subtitle_label = ctk.CTkLabel(
            card,
            text=subtitle,
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        subtitle_label.pack(pady=(5, 15))
    
    def _create_charts(self):
        """Create visualization charts."""
        # Weekly/Monthly summary
        self._create_summary_chart()
        
        # Category breakdown
        self._create_category_chart()
        
        # Completion trend
        self._create_trend_chart()
    
    def _create_summary_chart(self):
        """Create weekly/monthly summary chart."""
        chart_frame = ctk.CTkFrame(self)
        chart_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(
            chart_frame,
            text="Weekly & Monthly Summary",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10)
        
        weekly = self.stats_service.get_weekly_summary()
        monthly = self.stats_service.get_monthly_summary()
        
        fig = Figure(figsize=(8, 4), facecolor='none')
        ax = fig.add_subplot(111)
        
        categories = ['Total\nCompletions', 'Habits\nCompleted']
        weekly_data = [weekly['total_completions'], weekly['habits_completed']]
        monthly_data = [monthly['total_completions'], monthly['habits_completed']]
        
        x = range(len(categories))
        width = 0.35
        
        ax.bar([i - width/2 for i in x], weekly_data, width, label='This Week', color='#4ECDC4')
        ax.bar([i + width/2 for i in x], monthly_data, width, label='This Month', color='#45B7D1')
        
        ax.set_xlabel('Metrics')
        ax.set_ylabel('Count')
        ax.set_title('Activity Summary')
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.legend()
        ax.set_facecolor('none')
        fig.patch.set_facecolor('none')
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    def _create_category_chart(self):
        """Create category breakdown pie chart."""
        chart_frame = ctk.CTkFrame(self)
        chart_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(
            chart_frame,
            text="Category Breakdown (Last 30 Days)",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10)
        
        breakdown = self.stats_service.get_category_breakdown()
        
        if not breakdown:
            ctk.CTkLabel(
                chart_frame,
                text="No data available",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            ).pack(pady=20)
            return
        
        fig = Figure(figsize=(6, 6), facecolor='none')
        ax = fig.add_subplot(111)
        
        categories = list(breakdown.keys())
        values = list(breakdown.values())
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE']
        
        ax.pie(values, labels=categories, autopct='%1.1f%%', colors=colors[:len(categories)])
        ax.set_title('Completions by Category')
        ax.set_facecolor('none')
        fig.patch.set_facecolor('none')
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    def _create_trend_chart(self):
        """Create completion trend line chart."""
        chart_frame = ctk.CTkFrame(self)
        chart_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(
            chart_frame,
            text="Completion Trend (Last 30 Days)",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10)
        
        habits = self.db.get_all_habits()
        if not habits:
            ctk.CTkLabel(
                chart_frame,
                text="No habits to display",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            ).pack(pady=20)
            return
        
        fig = Figure(figsize=(10, 4), facecolor='none')
        ax = fig.add_subplot(111)
        
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        
        dates = [start_date + timedelta(days=i) for i in range(31)]
        total_completions = [0] * 31
        
        for habit in habits:
            trend = self.stats_service.get_completion_trend(habit.id, 30)
            for i, (comp_date, completed) in enumerate(trend):
                if completed:
                    total_completions[i] += 1
        
        ax.plot(dates, total_completions, marker='o', linewidth=2, markersize=4, color='#4ECDC4')
        ax.set_xlabel('Date')
        ax.set_ylabel('Daily Completions')
        ax.set_title('Daily Completion Trend')
        ax.grid(True, alpha=0.3)
        ax.set_facecolor('none')
        fig.patch.set_facecolor('none')
        
        # Rotate x-axis labels
        fig.autofmt_xdate()
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    def refresh(self):
        """Refresh all statistics."""
        for widget in self.winfo_children():
            widget.destroy()
        self._create_widgets()
