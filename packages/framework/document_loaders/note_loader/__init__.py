"""
Functions for loading and processing clinical progress notes.
"""

import re
from typing import Dict, Any, Optional, List, Union

def load_progress_note(note_content: str) -> Dict[str, Any]:
    """
    Load and preprocess a clinical progress note.
    
    Args:
        note_content: The raw content of the progress note
        
    Returns:
        Dict[str, Any]: Dictionary containing the parsed progress note sections
    """
    sections = parse_note_sections(note_content)
    
    return {
        "raw_content": note_content,
        "sections": sections,
        "assessment_plan": sections.get("Assessment / Plan", "")
    }

def parse_note_sections(note_content: str) -> Dict[str, str]:
    """
    Parse a progress note into sections based on headers.
    
    Args:
        note_content: The raw content of the progress note
        
    Returns:
        Dict[str, str]: Dictionary mapping section names to content
    """
    # Define section header pattern
    section_pattern = r"^([A-Za-z\/\s]+)$\n|(^[A-Za-z\/\s]+\s*[\-:]\s*$)"
    
    # Split the note into lines
    lines = note_content.split("\n")
    
    sections = {}
    current_section = "Header"
    current_content = []
    
    for line in lines:
        # Check if this line is a section header
        if re.match(section_pattern, line):
            # Save the previous section
            if current_content:
                sections[current_section] = "\n".join(current_content).strip()
                current_content = []
            
            # Set the new section name
            current_section = line.strip().split(':')[0].strip()
            
        else:
            # Add line to the current section content
            current_content.append(line)
    
    # Add the last section
    if current_content:
        sections[current_section] = "\n".join(current_content).strip()
    
    # If we couldn't find structured sections, use heuristics for Assessment / Plan
    if "Assessment / Plan" not in sections and "Assessment" not in sections:
        # Try to find the Assessment/Plan section by looking for patterns
        assessment_match = re.search(r"(?:Assessment|A/P|Assessment & Plan|Plan)(.*?)(?=\n\n|\Z)", 
                                     note_content, re.DOTALL | re.IGNORECASE)
        if assessment_match:
            sections["Assessment / Plan"] = assessment_match.group(1).strip()
    
    return sections

def extract_assessment_plan(sections: Dict[str, str]) -> str:
    """
    Extract the Assessment/Plan section from parsed note sections.
    
    Args:
        sections: Dictionary of note sections
        
    Returns:
        str: The Assessment/Plan section content
    """
    # Check for variations of Assessment/Plan section headers
    for header in ["Assessment / Plan", "Assessment/Plan", "Assessment & Plan", "A/P", "Plan"]:
        if header in sections:
            return sections[header]
    
    # If no specific Assessment/Plan section is found, return empty string
    return ""

def extract_condition_blocks(assessment_plan: str) -> List[str]:
    """
    Extract individual condition blocks from the Assessment/Plan section.
    
    Args:
        assessment_plan: The Assessment/Plan section content
        
    Returns:
        List[str]: List of individual condition blocks
    """
    # Try multiple patterns to match different formatting styles
    
    # Pattern 1: Number with period (e.g., "1. Condition")
    pattern1 = r"(?:^|\n)\s*(\d+\.\s*.*?)(?=(?:\n\s*\d+\.)|$)"
    
    # Pattern 2: Number with parenthesis (e.g., "1) Condition")
    pattern2 = r"(?:^|\n)\s*(\d+\)\s*.*?)(?=(?:\n\s*\d+\))|$)"
    
    # Pattern 3: General numbered list with dash (e.g., "1 - Condition")
    pattern3 = r"(?:^|\n)\s*(\d+\s*-\s*.*?)(?=(?:\n\s*\d+\s*-)|$)"
    
    # Try each pattern and use the one that finds the most blocks
    blocks1 = re.findall(pattern1, assessment_plan, re.DOTALL)
    blocks2 = re.findall(pattern2, assessment_plan, re.DOTALL)
    blocks3 = re.findall(pattern3, assessment_plan, re.DOTALL)
    
    # Use the pattern that found the most blocks
    if len(blocks1) >= len(blocks2) and len(blocks1) >= len(blocks3):
        blocks = blocks1
    elif len(blocks2) >= len(blocks1) and len(blocks2) >= len(blocks3):
        blocks = blocks2
    else:
        blocks = blocks3
    
    # If no blocks were found with the standard patterns, try a more aggressive approach
    if not blocks:
        # Look for any lines with ICD-10 codes (e.g., "F19.20" or "E78.5")
        icd_pattern = r"(?:^|\n)([^\n]*?(?:[A-Z]\d+\.\d+)[^\n]*(?:\n(?![A-Z]\d+\.\d+)[^\n]+)*)"
        blocks = re.findall(icd_pattern, assessment_plan, re.DOTALL)
    
    # Clean up each block
    return [block.strip() for block in blocks if block.strip()]