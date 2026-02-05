# ⚡ Axilium - Habit Tracker

A fun and engaging habit tracking desktop application built with Python and CustomTkinter.

## Features

- **📋 Habit Management**: Create, edit, and track multiple habits
- **🔥 Streak Tracking**: Build and maintain daily streaks
- **📊 Statistics**: Visual charts and insights into your progress
- **🎁 Rewards System**: Earn points and unlock rewards
- **⏰ Reminders**: Get notified to complete your habits
- **🎨 Themes**: Multiple beautiful themes to choose from
- **💾 Data Export**: Export your data to JSON or CSV
- **📈 Progress Tracking**: Visual progress bars and completion rates

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd axilium
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python run.py
   ```

## Building the Executable

To create a standalone Windows EXE:

1. Install PyInstaller (if not already installed):
   ```bash
   pip install pyinstaller
   ```

2. Run the build script:
   ```bash
   python build_exe.py
   ```

3. The executable will be created in the `dist` folder as `Axilium.exe`

## Usage

### Adding Habits

1. Click the "+ Add Habit" button
2. Fill in the habit details:
   - Name and description
   - Category (Health & Fitness, Learning, etc.)
   - Frequency (daily, weekly, custom)
   - Goals (days per week/month)
   - Optional reminder time
3. Click "Save"

### Tracking Habits

- Click the "✓ Complete" button on a habit card to mark it as done for today
- Your streak will automatically update
- Earn points for each completion

### Viewing Statistics

- Navigate to the "Statistics" tab to see:
  - Overall completion rate
  - Average streak length
  - Category breakdown charts
  - Completion trends over time

### Rewards

- Earn 10 points for each habit completion
- Unlock rewards at milestone point values
- View unlocked rewards in the "Rewards" tab

### Settings

- Change themes (Dark, Light, Ocean Blue, Purple Dream, Forest Green)
- Export your data to JSON or CSV
- Import data from a JSON backup
- Reset all data (use with caution!)

## Project Structure

```
axilium/
├── src/
│   ├── main.py              # Application entry point
│   ├── ui/                   # UI components
│   ├── models/               # Data models
│   ├── services/             # Business logic services
│   └── utils/                # Utilities and constants
├── assets/                   # Images and icons
├── data/                     # Database storage
├── requirements.txt          # Python dependencies
├── build_exe.py             # Build script for EXE
└── README.md                 # This file
```

## Technologies Used

- **CustomTkinter**: Modern UI framework
- **SQLite**: Database for data persistence
- **Matplotlib**: Data visualization
- **Plyer**: Cross-platform notifications
- **Schedule**: Reminder scheduling
- **PyInstaller**: Executable packaging

## License

This project is open source and available for personal use.

## Contributing

Feel free to fork this project and submit pull requests for improvements!

## Support

For issues or questions, please open an issue on the GitHub repository.

---

Made with ❤️ using Python and CustomTkinter
