"""
Test suite for the TimeBlock dataclass, refactored to use Pytest.
"""
import pytest
from datetime import datetime
from day_logger.models.timeblock import TimeBlock

def test_timeblock_creation_defaults():
    """Test creation with default date."""
    block_name = "Morning Tasks"
    start_time = "08:00"
    end_time = "12:00"
    content = "Sample tasks for the morning."
    tb = TimeBlock(block_name, start_time, end_time, content)
    
    assert tb.block_name == block_name
    assert tb.start_time == start_time
    assert tb.end_time == end_time
    assert tb.content == content
    assert isinstance(tb.date, datetime)

def test_timeblock_creation_custom_date():
    """Test creation with given date."""
    custom_date = datetime(2025, 2, 28)
    tb = TimeBlock(
        block_name="Evening Tasks",
        start_time="18:00",
        end_time="22:00",
        content="Evening tasks here",
        date=custom_date
    )
    assert tb.date == custom_date

def test_to_text_output():
    """Test the to_text() method for correct formatting."""
    tb = TimeBlock(
        block_name="Mid-day Tasks",
        start_time="12:00",
        end_time="13:00",
        content="Lunch break or errands"
    )
    output = tb.to_text()
    assert "Block: Mid-day Tasks" in output
    assert "Time: 12:00 - 13:00" in output
    assert "Lunch break or errands" in output

def test_to_json_output():
    """Test the to_json() method returns correct structure and data."""
    custom_date = datetime(2025, 2, 15)
    tb = TimeBlock(
        block_name="Evening Tasks",
        start_time="18:00",
        end_time="22:00",
        content="  Evening tasks here  ",  # Extra spaces to test stripping
        date=custom_date
    )
    json_data = tb.to_json()
    
    assert json_data["block_name"] == "Evening Tasks"
    assert json_data["start_time"] == "18:00"
    assert json_data["end_time"] == "22:00"
    assert json_data["content"] == "Evening tasks here"  # Should be stripped
    assert json_data["date"] == "2025-02-15T00:00:00"

def test_to_json_date_serialization():
    """Test that date serialization in JSON uses ISO format."""
    custom_date = datetime(2025, 2, 15, 14, 30, 45)  # Include time components
    tb = TimeBlock(
        block_name="Test Block",
        start_time="14:00",
        end_time="15:00",
        content="Test content",
        date=custom_date
    )
    json_data = tb.to_json()
    assert json_data["date"] == "2025-02-15T14:30:45"
