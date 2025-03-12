"""
Node for extracting medical conditions from condition blocks.
"""

import logging
import re
from typing import List

from packages.workflows.hcc_extractor.v0.agent.schemas.states import OverallState, Condition
from packages.workflows.hcc_extractor.v0.agent.schemas.format_instructions import ExtractedConditions
from packages.workflows.hcc_extractor.v0.agent.prompt_templates import condition_extraction_prompt
from packages.workflows.hcc_extractor.v0.utils.call_llm import call_llm

logger = logging.getLogger(__name__)

def condition_extractor(state: OverallState) -> OverallState:
    """
    Extract conditions from the identified condition blocks.
    
    Args:
        state: The current state containing condition blocks
        
    Returns:
        OverallState: Updated state with extracted conditions
    """
    logger.info("Extracting conditions from condition blocks")
    
    # Get the note and condition blocks from state
    note = state["note"]
    condition_blocks = note["condition_blocks"]
    
    if not condition_blocks:
        logger.warning("No condition blocks to process")
        return {"raw_conditions": []}
    
    # Get the full note content for context
    full_note_content = note.get("raw_content", "")
    assessment_plan = note.get("assessment_plan", "")
    
    # Join the condition blocks for processing
    joined_blocks = "\n\n".join(condition_blocks)
    
    # Create a more detailed prompt context
    prompt_context = {
        "condition_blocks": joined_blocks,
        "assessment_plan": assessment_plan,
        "full_note": full_note_content[:2000] if len(full_note_content) > 2000 else full_note_content
    }
    
    # Try using LLM for extraction
    try:
        # Extract conditions using LLM
        extracted: ExtractedConditions = call_llm(
            prompt_template=condition_extraction_prompt,
            input_parameters=prompt_context,
            pydantic_object=ExtractedConditions
        )
        
        # Convert to the internal Condition format
        raw_conditions: List[Condition] = [
            {
                "condition_code": condition.condition_code,
                "condition_name": condition.condition_name,
                "condition_data": condition.condition_data
            }
            for condition in extracted.conditions
        ]
        
        logger.info(f"Extracted {len(raw_conditions)} conditions")
    except Exception as e:
        logger.error(f"Error during LLM extraction: {str(e)}")
        raw_conditions = []
    
    # If no conditions were extracted, try a fallback approach using regex
    if not raw_conditions:
        logger.warning("No conditions extracted with LLM, trying fallback extraction")
        fallback_conditions = extract_conditions_with_regex(assessment_plan)
        
        if fallback_conditions:
            logger.info(f"Extracted {len(fallback_conditions)} conditions using fallback method")
            raw_conditions = fallback_conditions
    
    # Return updated state
    return {"raw_conditions": raw_conditions}

def extract_conditions_with_regex(text: str) -> List[Condition]:
    """
    Extract conditions using regex as a fallback method.
    
    Args:
        text: The text to extract conditions from
        
    Returns:
        List[Condition]: List of extracted conditions
    """
    conditions = []
    
    # Pattern 1: Find conditions with direct ICD-10 code format
    pattern1 = r"(\d+[\).]?\s*[-)]?\s*([^-\n]+)[-\s]*([A-Z]\d+\.\d+)[^\n]*(?:\n(?!^\d+[\).])[^\n]+)*)"
    
    # Pattern 2: General matcher for numbered items with code anywhere in the block
    pattern2 = r"(\d+[\).]?\s*([^-\n\d]+)(?:[^\n]*?)(?:[^\n]*?([A-Z]\d+\.\d+)[^\n]*?)(?:\n(?!^\d+[\).])[^\n]+)*)"
    
    # First try the direct pattern
    matches = list(re.finditer(pattern1, text, re.MULTILINE))
    
    # If that doesn't work, try the more general pattern
    if not matches:
        matches = list(re.finditer(pattern2, text, re.MULTILINE))
    
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
    
    # If still no conditions found, try a more aggressive approach
    if not conditions:
        # Look for lines with codes
        code_pattern = r"[A-Z]\d+\.\d+"
        code_matches = re.findall(code_pattern, text)
        
        for code in code_matches:
            # Find the line containing this code
            line_pattern = r"[^\n]*?" + re.escape(code) + r"[^\n]*"
            line_match = re.search(line_pattern, text)
            
            if line_match:
                line = line_match.group(0)
                # Extract condition name - everything before the code
                name_pattern = r"([^-\n]+)\s*[-]*\s*" + re.escape(code)
                name_match = re.search(name_pattern, line)
                
                if name_match:
                    condition_name = name_match.group(1).strip()
                else:
                    # Default name if extraction fails
                    condition_name = f"Condition with code {code}"
                
                # Add to conditions
                conditions.append({
                    "condition_code": code,
                    "condition_name": condition_name,
                    "condition_data": "Extracted from assessment plan"
                })
    
    return conditions