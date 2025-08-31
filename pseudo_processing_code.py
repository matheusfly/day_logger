import os
from datetime import datetime

def create_folder_structure(base_path, timestamp):
    # Parse timestamp into datetime object
    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    
    # Paths for each folder type
    year = dt.year
    month_folder = f"{str(year)[-2:]}-{dt.strftime('%m')}/"
    week_number = dt.strftime("%U")  # Week number
    week_folder = f"[w]{week_number}-{dt.strftime('%m-%d')}/"
    daily_folder = f"{dt.strftime('%a-%d-%m-%y')}/"
    
    # Full paths
    daily_path = os.path.join(base_path, "daily", daily_folder)
    monthly_path = os.path.join(base_path, "monthly", month_folder)
    weekly_path = os.path.join(base_path, "weekly", week_folder)
    
    # Create directories
    for path in [daily_path, monthly_path, weekly_path]:
        os.makedirs(path, exist_ok=True)
    
    return {
        "daily": daily_path,
        "monthly": monthly_path,
        "weekly": weekly_path
    }

# Example usage
base_directory = "work-logs/2024"
timestamp_example = "2024-12-03 10:00:00"
folders = create_folder_structure(base_directory, timestamp_example)

print(f"Daily Folder: {folders['daily']}")
print(f"Monthly Folder: {folders['monthly']}")
print(f"Weekly Folder: {folders['weekly']}")


''''### **How It Works**
1. The function `create_folder_structure` takes a base path and a timestamp.
2. It extracts the year, month, week number, and day to create folders dynamically.
3. It generates paths for daily, weekly, and monthly logs based on your naming conventions.
4. Uses `os.makedirs()` to ensure directories are created if they don't already exist.

You can use this as a blueprint to manage files effectively in your program. Let me know if you need further details or enhancements!
''''