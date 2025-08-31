"""
Output formatters module.
Contains functions for formatting and structuring output data.
"""

from typing import Any, Dict, List
import json
from datetime import datetime

class OutputFormatter:
    """Handles formatting of output data."""
    
    @staticmethod
    def to_json(data: Any, pretty: bool = False) -> str:
        """Convert data to JSON string."""
        if pretty:
            return json.dumps(data, indent=2, default=str)
        return json.dumps(data, default=str)
    
    @staticmethod
    def format_task_list(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format a list of tasks for output."""
        formatted = []
        for task in tasks:
            formatted.append({
                "id": task.get("id", ""),
                "title": task.get("title", ""),
                "due_date": task.get("due_date", ""),
                "created": task.get("created_at", datetime.now().isoformat())
            })
        return formatted
    
    @staticmethod
    def format_error(error: Exception, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Format error messages."""
        return {
            "error": str(error),
            "type": error.__class__.__name__,
            "timestamp": datetime.now().isoformat(),
            "context": context or {}
        }
