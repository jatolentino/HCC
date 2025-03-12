"""
Methods for extracting conditions from clinical notes.
"""

import re
from typing import List, Dict, Any, Optional

def extract_assessment_plan_section(note_content: str) -> Optional[str]:
    """
    Extract the Assessment/Plan section from a clinical note.
    
    Args:
        note_content: The full content of the clinical note
        
    Returns:
        Optional[str]: The Assessment/Plan section, or None if not found
    """
    # Look for Assessment/Plan section with some flexibility in heading format
    pattern = r"(?i)Assessment\s*(?:/|&|\+)\s*Plan\s*(?::|$)(.*?)(?:$|(?:\n\s*[A-Z][A-Za-z\s]*:))"
    match = re.search(pattern, note_content, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    
    # Try alternative format just in case
    pattern = r"(?i)Assessment and Plan\s*(?::|$)(.*?)(?:$|(?:\n\s*[A-Z][A-Za-z\s]*:))"
    match = re.search(pattern, note_content, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    
    # If we can't find a clear heading, look for numbered sections which indicate an assessment/plan
    pattern = r"(?:^|\n)\s*\d+\.\s*([^-\n]*)-\s*([^:]*?)(?:\n\s*\d+\.|$)"
    matches = re.finditer(pattern, note_content, re.MULTILINE)
    
    if matches:
        # Reconstruct the assessment/plan section
        assessment_plan = ""
        for match in matches:
            assessment_plan += match.group(0)
        
        if assessment_plan:
            return assessment_plan.strip()
    
    return None

def extract_condition_blocks(assessment_plan: str) -> List[str]:
    """
    Extract individual condition blocks from the Assessment/Plan section.
    
    Args:
        assessment_plan: The Assessment/Plan section content
        
    Returns:
        List[str]: List of individual condition blocks
    """
    # Look for numbered items with details
    pattern = r"(?:^|\n)\s*(\d+\.\s*.*?)(?=(?:\n\s*\d+\.)|$)"
    blocks = re.findall(pattern, assessment_plan, re.DOTALL)
    
    # Clean up each block
    return [block.strip() for block in blocks if block.strip()]