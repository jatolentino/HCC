"""
Test utility for importing CSV files.
"""

import csv
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def import_csv(file_path: str) -> List[Dict[str, Any]]:
    """
    Import data from a CSV file.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        List[Dict[str, Any]]: List of dictionaries containing the CSV data
    """
    result = []
    
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                result.append(row)
    
    except Exception as e:
        logger.error(f"Error importing CSV: {str(e)}")
        return []
    
    return result

def test_import_hcc_codes():
    """Test importing HCC codes from the CSV file."""
    csv_path = Path(__file__).parent.parent.parent / "HCC_relevant_codes.csv"
    
    if not csv_path.exists():
        logger.error(f"CSV file not found: {csv_path}")
        return
    
    data = import_csv(str(csv_path))
    
    logger.info(f"Imported {len(data)} rows from {csv_path}")
    logger.info(f"Sample data: {data[:3]}")
    
    # Verify the data
    assert len(data) > 0, "CSV file should not be empty"
    assert 'ICD-10-CM Codes' in data[0], "CSV file should have an 'ICD-10-CM Codes' column"
    assert 'Description' in data[0], "CSV file should have a 'Description' column"
    
    return data

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()]
    )
    
    # Run the test
    test_import_hcc_codes()