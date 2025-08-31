"""
Refactored test_journal_data_manager.py to use Pytest fixtures and remove unittest.
Covers JournalDataManager's functionality with temporary directories for clean testing.
"""

import pytest
import os
from datetime import datetime
from day_logger.journal_data_manager import JournalDataManager

@pytest.fixture
def mock_journal_instance():
    """
    Pytest fixture to simulate a task journal instance's widgets.
    """
    class _MockTextWidget:
        def __init__(self, value):
            self.value = value
        def get(self, start_idx, end_idx):
            return self.value

    class _MockWidget:
        def __init__(self, value):
            self.value = value
        def get(self):
            return self.value

    class MockTaskJournalInstance:
        def __init__(self):
            self.entry_widgets = {
                "morning": {
                    "start": _MockWidget("08:00"),
                    "end": _MockWidget("12:00"),
                    "text": _MockTextWidget("Morning tasks text")
                },
                "afternoon": {
                    "start": _MockWidget("13:00"),
                    "end": _MockWidget("17:00"),
                    "text": _MockTextWidget("Afternoon tasks text")
                }
            }
    return MockTaskJournalInstance()

@pytest.fixture
def data_manager(tmp_path):
    """
    Pytest fixture to create a JournalDataManager with a temporary directory as base_path.
    """
    return JournalDataManager(base_path=str(tmp_path))

def test_save_entry(data_manager, mock_journal_instance):
    """Test save_entry method to ensure it writes a JSON file with the correct structure."""
    success, message = data_manager.save_entry(mock_journal_instance)
    assert success
    assert "Entry saved successfully" in message

    # Verify the file was created and contains proper JSON
    file_found = False
    for root, _, files in os.walk(data_manager.base_path):
        for file in files:
            if file.endswith(".json"):
                file_found = True
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    import json
                    content = json.load(f)
                    assert "timestamp" in content
                    assert "time_blocks" in content
                    assert "morning" in content["time_blocks"]
                    assert "afternoon" in content["time_blocks"]
                    morning = content["time_blocks"]["morning"]
                    assert morning["start_time"] == "08:00"
                    assert morning["end_time"] == "12:00"
                    assert morning["content"] == "Morning tasks text"
    assert file_found, "No .json file was found in the directory structure."

def test_save_daily_timeblocks_new_file(data_manager, tmp_path):
    """Test saving timeblocks to a new JSON file."""
    from day_logger.models.timeblock import TimeBlock
    
    test_date = datetime(2025, 2, 15, 10, 30)
    blocks = [
        TimeBlock("Morning", "08:00", "12:00", "Test tasks", test_date),
        TimeBlock("Afternoon", "13:00", "17:00", "More tasks", test_date)
    ]
    
    success, message = data_manager.save_daily_timeblocks(blocks)
    assert success
    assert "Time blocks saved successfully" in message
    
    # Check the created file
    expected_file = tmp_path / "work-logs/2025/daily/2025-02-15.json"
    assert expected_file.exists()
    
    with open(expected_file, 'r', encoding='utf-8') as f:
        content = json.load(f)
        assert content["date"] == "2025-02-15"
        assert len(content["blocks"]) == 2
        assert "last_updated" in content
        
        block = content["blocks"][0]
        assert block["block_name"] == "Morning"
        assert block["start_time"] == "08:00"
        assert block["content"] == "Test tasks"

def test_save_daily_timeblocks_merge_existing(data_manager, tmp_path):
    """Test that saving timeblocks preserves existing blocks for the same day."""
    from day_logger.models.timeblock import TimeBlock
    
    test_date = datetime(2025, 2, 15, 10, 30)
    daily_path = tmp_path / "work-logs/2025/daily"
    daily_path.mkdir(parents=True, exist_ok=True)
    
    # Create initial file with one block
    initial_data = {
        "date": "2025-02-15",
        "blocks": [{
            "block_name": "Morning",
            "start_time": "08:00",
            "end_time": "12:00",
            "content": "Initial task",
            "date": "2025-02-15T08:00:00"
        }],
        "last_updated": "2025-02-15T08:00:00"
    }
    
    with open(daily_path / "2025-02-15.json", 'w', encoding='utf-8') as f:
        json.dump(initial_data, f)
    
    # Add new block
    new_blocks = [
        TimeBlock("Afternoon", "13:00", "17:00", "New task", test_date)
    ]
    
    success, _ = data_manager.save_daily_timeblocks(new_blocks)
    assert success
    
    # Verify both blocks exist
    with open(daily_path / "2025-02-15.json", 'r', encoding='utf-8') as f:
        content = json.load(f)
        assert len(content["blocks"]) == 2  # Both old and new blocks
        block_names = {b["block_name"] for b in content["blocks"]}
        assert block_names == {"Morning", "Afternoon"}

def test_load_latest_entry_no_file(data_manager):
    """Test load_latest_entry when no .json files exist (should return empty dict)."""
    data = data_manager.load_latest_entry()
    assert data == {}

def test_get_entries_by_date_empty(data_manager):
    """Test get_entries_by_date returns empty list when no JSON files exist."""
    result = data_manager.get_entries_by_date(datetime.now())
    assert isinstance(result, list)
    assert len(result) == 0

def test_load_latest_entry_with_file(data_manager, tmp_path):
    """Test load_latest_entry returns the most recent JSON entry."""
    import time
    
    # Create two entries with different timestamps
    entries_path = data_manager.base_path / "entries"
    entries_path.mkdir(parents=True)
    
    older_entry = {
        "timestamp": "2025-02-15T08:00:00",
        "time_blocks": {"morning": {"content": "Old entry"}}
    }
    newer_entry = {
        "timestamp": "2025-02-15T09:00:00",
        "time_blocks": {"morning": {"content": "New entry"}}
    }
    
    with open(entries_path / "old.json", 'w', encoding='utf-8') as f:
        json.dump(older_entry, f)
    time.sleep(0.1)  # Ensure different modification times
    with open(entries_path / "new.json", 'w', encoding='utf-8') as f:
        json.dump(newer_entry, f)
    
    latest = data_manager.load_latest_entry()
    assert latest["time_blocks"]["morning"]["content"] == "New entry"
