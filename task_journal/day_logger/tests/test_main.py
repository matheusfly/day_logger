"""
Test module for main functionality, refactored to use Pytest.
Contains unit tests for core functions.
"""

import pytest
from datetime import datetime, timedelta
from day_logger.main import process_data, validate_input

def test_process_data_valid():
    """Test processing valid data."""
    input_data = {"key": "value"}
    result = process_data(input_data)
    assert result is not None
    assert result["original_data"] == input_data
    assert result["status"] == "processed"

def test_process_data_invalid():
    """Test processing invalid data."""
    input_data = "invalid"
    result = process_data(input_data)
    assert result is None

def test_validate_input_valid():
    """Test validating valid input."""
    valid_data = [
        {
            "title": "Task 1",
            "description": "Description 1",
            "due_date": "2024-12-31"
        }
    ]
    is_valid, errors = validate_input(valid_data)
    assert is_valid
    assert len(errors) == 0

def test_validate_input_invalid():
    """Test validating invalid input."""
    invalid_data = "not a list"
    is_valid, errors = validate_input(invalid_data)
    assert not is_valid
    assert len(errors) > 0

def test_validate_input_missing_fields():
    """Test validation with missing required fields."""
    invalid_data = [{"title": "Task 1"}]  # Missing description
    is_valid, errors = validate_input(invalid_data)
    assert not is_valid
    assert any("missing required fields" in error for error in errors)
