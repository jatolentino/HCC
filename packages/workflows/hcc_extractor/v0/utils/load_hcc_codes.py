# """
# Utility for loading HCC-relevant codes from CSV.
# """

# import logging
# import os
# import csv
# from typing import List, Dict, Any
# from pathlib import Path

# logger = logging.getLogger(__name__)

# def load_hcc_codes(file_path: str = None) -> List[str]:
#     """
#     Load HCC-relevant codes from a CSV file.
    
#     Args:
#         file_path: Path to the CSV file, or None to use the default
        
#     Returns:
#         List[str]: List of HCC-relevant codes
#     """
#     # Use default path if not provided
#     if file_path is None:
#         file_path = "HCC_relevant_codes.csv"
    
#     # Make sure the file exists
#     if not Path(file_path).exists():
#         logger.warning(f"HCC codes file not found: {file_path}")
#         return []
    
#     # Load the codes
#     hcc_codes = []
    
#     try:
#         with open(file_path, 'r') as f:
#             reader = csv.DictReader(f)
            
#             # Check if the CSV has the expected format
#             if 'ICD-10-CM Codes' not in reader.fieldnames:
#                 logger.warning("CSV file does not have the expected format")
#                 return []
            
#             # Extract the codes
#             for row in reader:
#                 code = row['ICD-10-CM Codes'].strip()
#                 if code:
#                     hcc_codes.append(code)
    
#     except Exception as e:
#         logger.error(f"Error loading HCC codes: {str(e)}")
#         return []
    
#     logger.info(f"Loaded {len(hcc_codes)} HCC-relevant codes")
    
#     return hcc_codes


# v1
# """
# Utility for loading HCC-relevant codes from CSV.
# """

# import logging
# import os
# import csv
# from typing import List, Dict, Any
# from pathlib import Path

# logger = logging.getLogger(__name__)

# def load_hcc_codes(file_path: str = None) -> List[str]:
#     """
#     Load HCC-relevant codes from a CSV file.
    
#     Args:
#         file_path: Path to the CSV file, or None to use the default
        
#     Returns:
#         List[str]: List of HCC-relevant codes
#     """
#     # Use default path if not provided
#     if file_path is None:
#         file_path = "HCC_relevant_codes.csv"
    
#     # Make sure the file exists
#     if not Path(file_path).exists():
#         logger.warning(f"HCC codes file not found: {file_path}")
#         return []
    
#     # Load the codes
#     hcc_codes = []
    
#     try:
#         with open(file_path, 'r') as f:
#             reader = csv.DictReader(f)
            
#             # Check if the CSV has the expected format
#             if reader.fieldnames and 'ICD-10-CM Codes' not in reader.fieldnames:
#                 # Try to use the first column, whatever it is
#                 code_column = reader.fieldnames[0]
#                 logger.warning(f"CSV file does not have 'ICD-10-CM Codes' column, using '{code_column}' instead")
#             else:
#                 code_column = 'ICD-10-CM Codes'
            
#             # Extract the codes
#             for row in reader:
#                 if code_column in row:
#                     code = row[code_column].strip()
#                     if code:
#                         hcc_codes.append(code)
    
#     except Exception as e:
#         logger.error(f"Error loading HCC codes: {str(e)}")
#         return []
    
#     logger.info(f"Loaded {len(hcc_codes)} HCC-relevant codes")
    
#     return hcc_codes


# v2
"""
Utility for loading HCC-relevant codes from CSV.
"""

import logging
import os
import csv
from typing import List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

def load_hcc_codes(file_path: str = None) -> List[str]:
    """
    Load HCC-relevant codes from a CSV file.
    
    Args:
        file_path: Path to the CSV file, or None to use the default
        
    Returns:
        List[str]: List of HCC-relevant codes
    """
    # Use default path if not provided
    if file_path is None:
        file_path = "HCC_relevant_codes.csv"
    
    # Make sure the file exists
    if not Path(file_path).exists():
        logger.warning(f"HCC codes file not found: {file_path}")
        return []
    
    # Load the codes
    hcc_codes = []
    
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            
            # Check if the CSV has the expected format
            if reader.fieldnames and 'ICD-10-CM Codes' not in reader.fieldnames:
                # Try to use the first column, whatever it is
                code_column = reader.fieldnames[0]
                logger.warning(f"CSV file does not have 'ICD-10-CM Codes' column, using '{code_column}' instead")
            else:
                code_column = 'ICD-10-CM Codes'
            
            # Extract the codes
            for row in reader:
                if code_column in row:
                    code = row[code_column].strip()
                    if code:
                        # Ensure the code is properly formatted
                        hcc_codes.append(code)
    
    except Exception as e:
        logger.error(f"Error loading HCC codes: {str(e)}")
        return []
    
    # Log a few samples of loaded codes for debugging
    if hcc_codes:
        logger.info(f"Sample HCC codes loaded: {hcc_codes[:5]}")
    
    logger.info(f"Loaded {len(hcc_codes)} HCC-relevant codes")
    
    return hcc_codes

