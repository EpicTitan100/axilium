"""Theme definitions for Axilium."""

THEMES = {
    "dark": {
        "name": "Dark Mode",
        "bg_color": "#1a1a1a",
        "fg_color": "#2b2b2b",
        "text_color": "#ffffff",
        "accent_color": "#4ECDC4",
        "hover_color": "#3a3a3a",
        "border_color": "#404040"
    },
    "light": {
        "name": "Light Mode",
        "bg_color": "#f5f5f5",
        "fg_color": "#ffffff",
        "text_color": "#1a1a1a",
        "accent_color": "#4ECDC4",
        "hover_color": "#e0e0e0",
        "border_color": "#d0d0d0"
    },
    "blue": {
        "name": "Ocean Blue",
        "bg_color": "#0a1929",
        "fg_color": "#132f4c",
        "text_color": "#e3f2fd",
        "accent_color": "#42a5f5",
        "hover_color": "#1e3a5f",
        "border_color": "#2a4a6f"
    },
    "purple": {
        "name": "Purple Dream",
        "bg_color": "#1a0d2e",
        "fg_color": "#2d1b3d",
        "text_color": "#f3e5f5",
        "accent_color": "#ab47bc",
        "hover_color": "#3d2b4d",
        "border_color": "#4d3b5d"
    },
    "green": {
        "name": "Forest Green",
        "bg_color": "#0d1f0d",
        "fg_color": "#1a3a1a",
        "text_color": "#e8f5e9",
        "accent_color": "#66bb6a",
        "hover_color": "#2a4a2a",
        "border_color": "#3a5a3a"
    }
}

DEFAULT_THEME = "dark"

def get_theme(theme_name: str = None) -> dict:
    """Get theme configuration by name."""
    if theme_name is None:
        theme_name = DEFAULT_THEME
    return THEMES.get(theme_name, THEMES[DEFAULT_THEME])
