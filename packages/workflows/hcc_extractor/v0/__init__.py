"""
HCC Extractor workflow for processing clinical progress notes.
"""

import logging
import os
import re
import json
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

def normalize_code(code: str) -> str:
    """Normalize an ICD-10 code by removing dots and converting to uppercase."""
    return code.replace(".", "").upper()

def run_hcc_extractor_v0(
    note_content: str,
) -> List[Dict[str, Any]]:
    """
    Process a clinical progress note to extract HCC-relevant conditions.
    
    Args:
        note_content: The content of the progress note
        
    Returns:
        List[Dict[str, Any]]: List of extracted conditions with HCC relevance
    """
    from packages.workflows.hcc_extractor.v0.agent import hcc_extraction_agent
    from packages.workflows.hcc_extractor.v0.utils.load_hcc_codes import load_hcc_codes
    from packages.workflows.hcc_extractor.v0.agent.nodes.condition.extraction import extract_conditions_with_regex

    logger.info("Starting HCC extraction process")
    
    # Load HCC codes
    hcc_codes = load_hcc_codes()
    
    # Normalize HCC codes for better matching
    normalized_hcc_code_set = set()
    for code in hcc_codes:
        # Normalize the code: remove dots and make uppercase
        normalized_code = normalize_code(code)
        normalized_hcc_code_set.add(normalized_code)
        # Also add the original code for exact matches
        normalized_hcc_code_set.add(code.upper())
    
    # Log some sample codes for debugging
    logger.info(f"Sample normalized HCC codes: {list(normalized_hcc_code_set)[:5] if len(normalized_hcc_code_set) > 5 else list(normalized_hcc_code_set)}")
    
    # Check for specific codes (for debugging)
    test_codes = ["F19.20", "F1920", "K51.90", "K5190"]
    for test_code in test_codes:
        normalized_test = normalize_code(test_code)
        logger.info(f"Code {test_code} normalized to {normalized_test} is {'IN' if normalized_test in normalized_hcc_code_set else 'NOT IN'} HCC set")
    
    # Check if we should use the fallback extraction method directly
    use_fallback = os.getenv("USE_FALLBACK_EXTRACTION", "").lower() in ("true", "1", "yes")
    
    if use_fallback:
        logger.info("Using direct fallback extraction (skipping LLM)")
        # Extract the assessment plan section manually
        assessment_plan = None
        
        # Look for the Assessment / Plan section
        lines = note_content.split('\n')
        for i, line in enumerate(lines):
            if "Assessment" in line and ("Plan" in line or "/" in line):
                assessment_plan = '\n'.join(lines[i+1:])
                break
        
        # If found, extract conditions directly
        if assessment_plan:
            conditions = extract_conditions_with_regex(assessment_plan)
            
            # Validate conditions
            validated_conditions = []
            for condition in conditions:
                code = condition["condition_code"]
                # Normalize the condition code the same way
                normalized_code = normalize_code(code)
                
                # Check both original and normalized code formats
                original_in_set = code.upper() in normalized_hcc_code_set
                normalized_in_set = normalized_code in normalized_hcc_code_set
                is_hcc = original_in_set or normalized_in_set
                
                logger.info(f"Condition {code} (normalized: {normalized_code}) - HCC status: {is_hcc} (original match: {original_in_set}, normalized match: {normalized_in_set})")
                
                validated_conditions.append({
                    "condition_code": code,
                    "condition_name": condition["condition_name"],
                    "is_hcc": is_hcc,
                    "condition_data": condition["condition_data"]
                })
            
            logger.info(f"Extraction complete. Found {len(validated_conditions)} conditions.")
            logger.info(f"Validated conditions: {json.dumps(validated_conditions, indent=2)}")
            return validated_conditions
    
    # Use the LangGraph agent if fallback is not enabled or didn't find conditions
    try:
        # Invoke the HCC extraction agent
        result = hcc_extraction_agent.invoke(
            {
                "note_content": note_content,
                "hcc_codes": hcc_codes,
                "normalized_hcc_code_set": normalized_hcc_code_set,  # Pass the normalized set to the agent
            },
            {"recursion_limit": 100}
        )
        
        logger.info(f"Extraction complete. Found {len(result['conditions'])} conditions.")
        logger.info(f"Agent-validated conditions: {json.dumps(result['conditions'], indent=2)}")
        
        return result["conditions"]
        
    except Exception as e:
        logger.error(f"Error in HCC extraction agent: {str(e)}")
        
        # If the agent fails, use the fallback method
        logger.info("Falling back to direct extraction after agent failure")
        
        # Extract the assessment plan section manually
        assessment_plan = None
        
        # Look for the Assessment / Plan section
        lines = note_content.split('\n')
        for i, line in enumerate(lines):
            if "Assessment" in line and ("Plan" in line or "/" in line):
                assessment_plan = '\n'.join(lines[i+1:])
                break
        
        # If found, extract conditions directly
        if assessment_plan:
            # Directly implement the extraction here to avoid import issues
            conditions = []
            
            # Pattern 1: Find conditions with direct ICD-10 code format
            pattern1 = r"(\d+[\).]?\s*[-)]?\s*([^-\n]+)[-\s]*([A-Z]\d+\.\d+)[^\n]*(?:\n(?!^\d+[\).])[^\n]+)*)"
            
            # Pattern 2: General matcher for numbered items with code anywhere in the block
            pattern2 = r"(\d+[\).]?\s*([^-\n\d]+)(?:[^\n]*?)(?:[^\n]*?([A-Z]\d+\.\d+)[^\n]*?)(?:\n(?!^\d+[\).])[^\n]+)*)"
            
            # First try the direct pattern
            matches = list(re.finditer(pattern1, assessment_plan, re.MULTILINE))
            
            # If that doesn't work, try the more general pattern
            if not matches:
                matches = list(re.finditer(pattern2, assessment_plan, re.MULTILINE))
            
            for match in matches:
                full_block = match.group(1).strip()
                condition_name = match.group(2).strip()
                condition_code = match.group(3).strip()
                
                # Extract the condition data by removing the condition name and code
                data_lines = []
                for line in full_block.split('\n'):
                    if condition_name not in line and condition_code not in line:
                        # Remove leading numbers and punctuation
                        cleaned_line = re.sub(r"^\d+[\).\s-]+", "", line).strip()
                        if cleaned_line:
                            data_lines.append(cleaned_line)
                
                condition_data = "\n".join(data_lines)
                
                # If no condition data was extracted, use a generic message
                if not condition_data:
                    condition_data = "No specific management details provided"
                
                conditions.append({
                    "condition_code": condition_code,
                    "condition_name": condition_name,
                    "condition_data": condition_data
                })
            
            # Validate conditions
            validated_conditions = []
            for condition in conditions:
                code = condition["condition_code"]
                # Normalize the condition code the same way
                normalized_code = normalize_code(code)
                
                # Check both original and normalized code formats
                original_in_set = code.upper() in normalized_hcc_code_set
                normalized_in_set = normalized_code in normalized_hcc_code_set
                is_hcc = original_in_set or normalized_in_set
                
                logger.info(f"Condition {code} (normalized: {normalized_code}) - HCC status: {is_hcc} (original match: {original_in_set}, normalized match: {normalized_in_set})")
                
                validated_conditions.append({
                    "condition_code": code,
                    "condition_name": condition["condition_name"],
                    "is_hcc": is_hcc,
                    "condition_data": condition["condition_data"]
                })
            
            logger.info(f"Fallback extraction complete. Found {len(validated_conditions)} conditions.")
            logger.info(f"Fallback-validated conditions: {json.dumps(validated_conditions, indent=2)}")
            return validated_conditions
        
        # If nothing worked, return empty list
        return []