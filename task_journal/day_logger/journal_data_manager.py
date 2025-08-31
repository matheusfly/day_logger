import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

class JournalDataManager:
    def __init__(self, base_path: str = "journal_entries"):
        """Initialize the data manager with base path for saving entries."""
        self.base_path = Path(base_path)
        self._ensure_base_directory()

    def _ensure_base_directory(self) -> None:
        """Create base directory structure if it doesn't exist."""
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _create_timestamp_folders(self) -> Path:
        """Create timestamp-based folder structure and return the path."""
        now = datetime.now()
        
        # Create folder paths
        year_month = now.strftime("%y-%m")  # YY-MM
        week_folder = f"w{now.strftime('%V')}-{now.strftime('%m-%d')}"  # [w]ww-MM-dd
        day_folder = now.strftime("%a-%d-%m-%y")  # ddd-DD-MM-YY
        
        # Create complete path
        entry_path = self.base_path / year_month / week_folder / day_folder
        entry_path.mkdir(parents=True, exist_ok=True)
        
        return entry_path

    def collect_entry_data(self, task_journal_instance) -> Dict[str, Any]:
        """Collect all data from the task journal widgets using stored references."""
        entry_data = {
            "timestamp": datetime.now().isoformat(),
            "time_blocks": {}
        }
 
        for key, widgets in task_journal_instance.entry_widgets.items():
            start_time = widgets["start"].get()
            end_time = widgets["end"].get()
            content = widgets["text"].get('1.0', 'end-1c')
            placeholder = f"Enter your {key} tasks here..."
            if content.strip() == placeholder:
                content = ""
            entry_data["time_blocks"][key] = {
                "start_time": start_time,
                "end_time": end_time,
                "content": content
            }
 
        return entry_data

    def save_entry(self, task_journal_instance) -> tuple[bool, str]:
        """Save the journal entry to a JSON file."""
        try:
            # Collect the data
            entry_data = self.collect_entry_data(task_journal_instance)
            
            # Create timestamp folders
            entry_path = self._create_timestamp_folders()
            
            # Create filename with timestamp
            now = datetime.now()
            filename = f"journal_entry_{now.strftime('%H-%M-%S')}.json"
            
            # Save the entry as a JSON file
            file_path = entry_path / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(entry_data, f, indent=2)
            
            return True, f"Entry saved successfully to {file_path}"

        except Exception as e:
            return False, f"Error saving entry: {str(e)}"

    def load_latest_entry(self) -> Dict[str, Any]:
        """Load the most recent journal entry."""
        try:
            # Find the most recent entry
            latest_file = None
            latest_time = None
            
            for root, _, files in os.walk(self.base_path):
                for file in files:
                    if file.endswith('.json'):
                        file_path = Path(root) / file
                        file_time = file_path.stat().st_mtime
                        
                        if latest_time is None or file_time > latest_time:
                            latest_time = file_time
                            latest_file = file_path

            if latest_file:
                with open(latest_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            return {}

        except Exception as e:
            print(f"Error loading latest entry: {str(e)}")
            return {}

    def get_entries_by_date(self, date: datetime) -> list[Dict[str, Any]]:
        """Retrieve all entries for a specific date."""
        try:
            # Create the path for the specified date
            year_month = date.strftime("%y-%m")
            week_folder = f"w{date.strftime('%V')}-{date.strftime('%m-%d')}"
            day_folder = date.strftime("%a-%d-%m-%y")
            
            target_path = self.base_path / year_month / week_folder / day_folder
            
            entries = []
            if target_path.exists():
                for file in target_path.glob("*.json"):
                    with open(file, 'r', encoding='utf-8') as f:
                        entries.append(json.load(f))
            
            return entries

        except Exception as e:
            print(f"Error retrieving entries: {str(e)}")
        return []

    def save_daily_timeblocks(self, blocks: list["TimeBlock"]) -> tuple[bool, str]:
        """
        Save a list of time blocks to the 'work-logs/2025/daily' folder,
        storing them in a JSON file named after the date (YYYY-MM-DD.json).
        
        Args:
            blocks (list[TimeBlock]): The list of TimeBlock objects to save.
        
        Returns:
            (bool, str): A tuple containing a success flag and a message.
        """
        try:
            from pathlib import Path
            daily_path = Path('work-logs/2025/daily')
            daily_path.mkdir(parents=True, exist_ok=True)
            
            if not blocks:
                return False, "No blocks to save."
            
            date_str = blocks[0].date.strftime("%Y-%m-%d")
            filename = f"{date_str}.json"
            file_path = daily_path / filename
            
            # Convert blocks to JSON format
            blocks_data = {
                "date": date_str,
                "blocks": [block.to_json() for block in blocks],
                "last_updated": datetime.now().isoformat()
            }
            
            # Save as JSON, preserving any existing blocks for the same day
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                    existing_blocks = existing_data.get("blocks", [])
                    blocks_data["blocks"].extend(existing_blocks)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(blocks_data, f, indent=2)
            
            return True, f"Time blocks saved successfully to {file_path}"
        except Exception as e:
            return False, f"Error saving time blocks: {str(e)}"
