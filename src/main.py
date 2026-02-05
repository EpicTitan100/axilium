"""Main entry point for Axilium."""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import customtkinter as ctk
from src.ui.main_window import MainWindow


def main():
    """Launch the Axilium application."""
    # Set appearance mode and color theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Create and run application
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
