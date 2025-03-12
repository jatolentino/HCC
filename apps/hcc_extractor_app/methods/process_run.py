"""
Methods for processing and extracting conditions from progress notes.
"""

import os
import logging
from typing import Dict, List, Any, Callable
from pathlib import Path

logger = logging.getLogger(__name__)

def process_progress_notes(extractor_function: Callable) -> Dict[str, List[Dict[str, Any]]]:
    """
    Process all progress notes in the progress_notes directory.
    
    Args:
        extractor_function: The function to use for extraction
        
    Returns:
        Dict[str, List[Dict[str, Any]]]: Dictionary mapping filenames to extracted conditions
    """
    results = {}
    progress_notes_dir = Path("progress_notes")
    
    # Check if the directory exists
    if not progress_notes_dir.exists():
        logger.error(f"Directory {progress_notes_dir} does not exist")
        return results
    
    # Process each progress note
    for note_file in progress_notes_dir.iterdir():
        if note_file.is_file():
            logger.info(f"Processing {note_file.name}")
            
            try:
                # Read the progress note content
                with open(note_file, "r") as f:
                    note_content = f.read()
                
                # Process the progress note
                result = extractor_function(note_content=note_content)
                
                # Store the result
                results[note_file.name] = result
                
                logger.info(f"Successfully processed {note_file.name}")
            except Exception as e:
                logger.error(f"Error processing {note_file.name}: {str(e)}")
                # Store empty results if there's an error
                results[note_file.name] = []
    
    return results