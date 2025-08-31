"""
Data processor module.
Contains classes and functions for processing input data.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    """Handles data processing and transformation."""
    
    def __init__(self):
        self.processed_count = 0
        self.error_count = 0
        
    def process_batch(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process a batch of items."""
        results = []
        for item in items:
            try:
                processed = self.process_item(item)
                if processed:
                    results.append(processed)
                    self.processed_count += 1
            except Exception as e:
                logger.error(f"Error processing item: {str(e)}")
                self.error_count += 1
        return results
    
    def process_item(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process a single item."""
        if not item:
            return None
            
        # Apply transformations
        processed = {
            "timestamp": datetime.now().isoformat(),
            "raw_data": item,
            "processed_fields": {},
            "metadata": {
                "source": item.get("source", "unknown"),
                "version": "1.0"
            }
        }
        
        # Process each field
        for key, value in item.items():
            if isinstance(value, str):
                processed["processed_fields"][key] = value.strip().lower()
            elif isinstance(value, (int, float)):
                processed["processed_fields"][key] = value
            elif isinstance(value, list):
                processed["processed_fields"][key] = [
                    str(x).strip() if isinstance(x, str) else x 
                    for x in value if x is not None
                ]
                
        return processed
