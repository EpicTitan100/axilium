# Quick Start Guide

## First Time Setup

1. **Install Python** (if not already installed)
   - Download from https://www.python.org/downloads/
   - Make sure to check "Add Python to PATH" during installation

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python run.py
   ```

## Creating Your First Habit

1. Click the **"+ Add Habit"** button
2. Enter a habit name (e.g., "Drink Water")
3. Choose a category
4. Select frequency (daily, weekly, or custom)
5. Set your goals
6. Click **"Save"**

## Completing Habits

- Click the **"✓ Complete"** button on any habit card
- Your streak will automatically update
- You'll earn 10 points per completion

## Tips

- **Build Streaks**: Complete habits daily to maintain your streak!
- **Set Reminders**: Enable reminders to never forget your habits
- **Track Progress**: Check the Statistics tab to see your progress
- **Earn Rewards**: Unlock rewards as you accumulate points
- **Export Data**: Regularly export your data as a backup

## Troubleshooting

### Application won't start
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check that you're running Python 3.8 or higher: `python --version`

### Notifications not working
- On Windows, make sure notifications are enabled in system settings
- The app will still work without notifications

### Database errors
- The database is created automatically in the `data` folder
- If you encounter errors, try deleting `data/axilium.db` and restarting

## Building the EXE

To create a standalone executable:

```bash
python build_exe.py
```

The executable will be in the `dist` folder.

## Need Help?

Check the main README.md for more detailed information.
