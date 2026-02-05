"""Constants for the Axilium application."""

# App Info
APP_NAME = "Axilium"
APP_VERSION = "1.0.0"

# Database
DB_NAME = "axilium.db"
import os
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "axilium.db")

# Habit Categories
CATEGORIES = [
    "Health & Fitness",
    "Learning",
    "Productivity",
    "Social",
    "Creative",
    "Mindfulness",
    "Other"
]

# Habit Frequencies
FREQUENCIES = ["daily", "weekly", "custom"]

# Default Colors for Categories
CATEGORY_COLORS = {
    "Health & Fitness": "#FF6B6B",
    "Learning": "#4ECDC4",
    "Productivity": "#45B7D1",
    "Social": "#FFA07A",
    "Creative": "#98D8C8",
    "Mindfulness": "#F7DC6F",
    "Other": "#BB8FCE"
}

# Reward Points
POINTS_PER_COMPLETION = 10
REWARD_MILESTONES = [50, 100, 250, 500, 1000, 2500, 5000]

# UI Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600

# Animation
ANIMATION_DURATION = 300  # milliseconds
