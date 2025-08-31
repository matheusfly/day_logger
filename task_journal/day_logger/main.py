"""
Main module for the application.
Contains core functionality and entry points.
"""
import logging
import uuid
import json
from typing import Any, Dict, List, Optional
from datetime import datetime
from day_logger.processors.data_processor import DataProcessor
from day_logger.utils.formatters import OutputFormatter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_data(input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Process incoming data and transform it according to business rules.
    
    Args:
        input_data (Dict[str, Any]): Raw input data dictionary
        
    Returns:
        Optional[Dict[str, Any]]: Processed data or None if processing fails
    """
    logger.info("Starting data processing")
    if not isinstance(input_data, dict):
        logger.error("Invalid input type; expected dictionary")
        return None

    processor = DataProcessor()
    processed = processor.process_item(input_data)
    if not processed:
        return None

    result = {
        "original_data": input_data,
        "processed_at": datetime.now().isoformat(),
        "status": "processed",
        "processed_data": processed,
        "metadata": {
            "processor_stats": {
                "processed": processor.processed_count,
                "errors": processor.error_count
            }
        }
    }
    logger.info("Data processing completed successfully.")
    return result

def validate_input(data: List[Dict[str, Any]]) -> tuple[bool, List[str]]:
    """
    Validate input data against required schema.
    
    Args:
        data (List[Dict[str, Any]]): List of data dictionaries to validate
        
    Returns:
        (bool, List[str]): A tuple containing a validity boolean and a list of error messages
    """
    logger.info("Starting input validation")
    errors = []
    try:
        if not isinstance(data, list):
            errors.append("Input must be a list")
            return False, errors

        for idx, item in enumerate(data):
            if not isinstance(item, dict):
                errors.append(f"Item at index {idx} must be a dictionary")
                continue

            # Validate required fields
            required_fields = ['title', 'description']
            missing_fields = [field for field in required_fields if field not in item]
            if missing_fields:
                errors.append(f"Item at index {idx} missing required fields: {missing_fields}")

            # Validate date format if present
            if 'due_date' in item and item['due_date']:
                from day_logger.utils.helpers import validate_date_format
                if not validate_date_format(item['due_date']):
                    errors.append(f"Item at index {idx} has invalid due_date format")

        is_valid = len(errors) == 0
        if is_valid:
            logger.info("Input validation successful")
        else:
            logger.error(f"Validation failed with {len(errors)} errors")

        return is_valid, errors

    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        errors.append(str(e))
        return False, errors
