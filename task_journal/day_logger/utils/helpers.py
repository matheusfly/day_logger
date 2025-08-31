"""
Utility functions module.
Contains helper functions used across the application.
"""

from typing import Any, Dict, List
from datetime import datetime
import json
import os


def load_config(config_path: str) -> dict:
    """
    Load configuration from a JSON file.

    Args:
        config_path (str): Path to the configuration file

    Returns:
        dict: Configuration dictionary

    Raises:
        FileNotFoundError: If config file doesn't exist
        json.JSONDecodeError: If config file is invalid JSON
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, 'r') as f:
        return json.load(f)


def batch_process(items: List[Any], batch_size: int = 100) -> List[List[Any]]:
    """
    Split a list of items into batches for processing.

    Args:
        items (List[Any]): List of items to batch
        batch_size (int): Size of each batch

    Returns:
        List[List[Any]]: List of batches
    """
    return [items[i:i + batch_size] for i in range(0, len(items), batch_size)]


def validate_date_format(date_str: str) -> bool:
    """
    Validate if a string is in correct ISO date format.

    Args:
        date_str (str): Date string to validate

    Returns:
        bool: True if valid ISO format, False otherwise
    """
    try:
        datetime.fromisoformat(date_str)
        return True
    except ValueError:
        return False


def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize input data by removing empty values and trimming strings.

    Args:
        data (Dict[str, Any]): Input dictionary

    Returns:
        Dict[str, Any]: Sanitized dictionary
    """
    return {
        k: v.strip() if isinstance(v, str) else v
        for k, v in data.items()
        if v is not None and (not isinstance(v, str) or v.strip())
    }
