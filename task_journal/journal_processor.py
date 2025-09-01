import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from day_logger.journal_data_manager import JournalDataManager
from day_logger.models.timeblock import TimeBlock
class JournalProcessor:
    def __init__(self, base_path: str = "work-logs"):
        """Initialize the processor with paths and data manager."""
        self.base_path = Path(base_path)
        self.data_manager = JournalDataManager(base_path)
        self.current_year = datetime.now().year
        self._ensure_folder_structure()

    def _ensure_folder_structure(self) -> None:
        """Create the base folder structure if it doesn't exist."""
        year_folder = self.base_path / str(self.current_year)
        
        # Create main folders
        for folder in ['daily', 'weekly', 'monthly']:
            (year_folder / folder).mkdir(parents=True, exist_ok=True)

    def _calculate_duration(self, start_time: str, end_time: str) -> float:
        """Calculate duration between two time strings in hours."""
        try:
            start = datetime.strptime(start_time, "%H:%M")
            end = datetime.strptime(end_time, "%H:%M")
            duration = end - start
            return round(duration.total_seconds() / 3600, 2)  # Convert to hours
        except ValueError:
            return 0.0

    def _extract_keywords(self, content: str) -> list[str]:
        """Extract relevant keywords from content."""
        # Simple keyword extraction (can be enhanced with NLP)
        words = content.lower().split()
        # Filter common words and keep relevant ones
        keywords = [word for word in words if len(word) > 3 and not word.isspace()]
        return list(set(keywords))[:5]  # Return up to 5 unique keywords

    def _count_tasks(self, content: str) -> int:
        """Count number of tasks in content (assumes tasks are separated by newlines)."""
        return len([line for line in content.split('\n') if line.strip()])

    def _generate_summary(self, time_blocks: Dict[str, TimeBlock]) -> str:
        """Generate a brief summary of the journal entry."""
        total_tasks = sum(block.tasks_count for block in time_blocks.values())
        total_duration = sum(block.duration for block in time_blocks.values())
        
        return (f"Daily journal entry with {total_tasks} tasks "
                f"spanning {total_duration:.1f} hours across "
                f"{len(time_blocks)} time blocks.")

    def build_timeblocks(self, raw_entry: Dict[str, Any]) -> list[TimeBlock]:
        """
        Convert raw journal entry data into a list of TimeBlock objects,
        using start/end times from spinboxes and content from text areas.
        Also applies business rules like extracting keywords or counting tasks if desired.
        """
        blocks = []
        for block_name, block_data in raw_entry["time_blocks"].items():
            # We can parse or convert times if needed (already done by _calculate_duration in older code).
            start_time = block_data["start_time"]
            end_time = block_data["end_time"]
            content = block_data["content"]
            
            # Construct a TimeBlock. We won't track 'keywords' or 'tasks_count' separately here,
            # but you can adopt that logic if desired.
            new_block = TimeBlock(
                block_name=block_name.title() + " Tasks",
                start_time=start_time,
                end_time=end_time,
                content=content,
                date=datetime.now()  # or parse from raw_entry if you want a specific date
            )
            blocks.append(new_block)
        return blocks


    def process_and_save_journal(self, task_journal_instance) -> tuple[bool, str]:
        """
        Main method to build TimeBlock objects from raw entry data,
        then save them in daily text files via JournalDataManager.
        """
        try:
            # 1) Collect raw data from the GUI
            raw_entry = self.data_manager.collect_entry_data(task_journal_instance)
            
            # 2) Build TimeBlock objects
            time_blocks = self.build_timeblocks(raw_entry)
            
            # 3) Use the data manager to save daily time blocks
            success, message = self.data_manager.save_daily_timeblocks(time_blocks)
            return success, message
        except Exception as e:
            return False, f"Error processing journal: {str(e)}"

    def process_and_save_journal_from_data(self, data: Dict[str, Any]) -> tuple[bool, str]:
        """
        Main method to build TimeBlock objects from raw entry data,
        then save them in daily text files via JournalDataManager.
        This method is intended to be used when data is passed directly, e.g. from an API.
        """
        try:
            # Data is expected to have a "time_blocks" key.
            time_blocks = self.build_timeblocks(data)

            # Use the data manager to save daily time blocks
            success, message = self.data_manager.save_daily_timeblocks(time_blocks)
            return success, message
        except Exception as e:
            return False, f"Error processing journal: {str(e)}"

if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) > 1:
        json_data = sys.argv[1]
        try:
            data = json.loads(json_data)
            # The data from the frontend is the value for "time_blocks".
            # I need to wrap it.
            entry_data = {"time_blocks": data}

            processor = JournalProcessor()
            success, message = processor.process_and_save_journal_from_data(entry_data)
            print(json.dumps({"success": success, "message": message}))
        except json.JSONDecodeError:
            print(json.dumps({"success": False, "message": "Invalid JSON format"}))
        except Exception as e:
            print(json.dumps({"success": False, "message": f"An error occurred: {e}"}))
    else:
        print(json.dumps({"success": False, "message": "No data provided"}))
