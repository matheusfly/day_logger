from dataclasses import dataclass
from datetime import datetime

@dataclass
class TimeBlock:
    """
    Represents a block of time-based tasks in a single day.
    
    Attributes:
        block_name: e.g. "Morning Tasks", "Mid-day Tasks", "Evening Tasks"
        start_time: string from spinbox e.g. "08:00"
        end_time:   string from spinbox e.g. "12:00"
        content:    actual user-entered text describing tasks
        date:       date (defaults to current date if not given)
    """
    block_name: str
    start_time: str
    end_time: str
    content: str
    date: datetime = datetime.now()
    
    def to_text(self) -> str:
        """
        Returns a formatted text representation of the time block.
        """
        return (
            f"Block: {self.block_name}\n"
            f"Time: {self.start_time} - {self.end_time}\n"
            f"Content:\n{self.content.strip()}\n"
            f"{'-'*40}\n"
        )
        
    def to_json(self) -> dict:
        """
        Returns a JSON-serializable dictionary representation of the time block.
        """
        return {
            "block_name": self.block_name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "content": self.content.strip(),
            "date": self.date.isoformat()
        }
