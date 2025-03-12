"""
Node for validating conditions against HCC-relevant codes.
"""

import logging
import json
from typing import List, Dict, Any

from packages.workflows.hcc_extractor.v0.agent.schemas.states import (
    OverallState, InputState, Condition, ValidatedCondition
)
from packages.workflows.hcc_extractor.v0.agent.schemas.format_instructions import ValidatedCondition as ValidatedConditionSchema
from packages.workflows.hcc_extractor.v0.agent.prompt_templates import hcc_validation_prompt
from packages.workflows.hcc_extractor.v0.utils.call_llm import call_llm

logger = logging.getLogger(__name__)

# def condition_validator(state: OverallState) -> OverallState:
#     """
#     Validate conditions against HCC-relevant codes.
    
#     Args:
#         state: The current state containing extracted conditions
        
#     Returns:
#         OverallState: Updated state with validated conditions
#     """
#     logger.info("Validating conditions against HCC-relevant codes")
    
#     # Get the raw conditions from state
#     raw_conditions = state.get("raw_conditions", [])
    
#     if not raw_conditions:
#         logger.warning("No conditions to validate")
#         return {"conditions": []}
    
#     # Get HCC codes from input state
#     input_state = state.get("_input", {})
#     hcc_codes = input_state.get("hcc_codes", [])
    
#     # Create set for faster lookup
#     hcc_code_set = set(hcc_codes) if hcc_codes else set()
    
#     # Always use the direct validation approach since it's more reliable
#     validated_conditions: List[ValidatedCondition] = []
    
#     for condition in raw_conditions:
#         code = condition["condition_code"]
        
#         validated_condition: ValidatedCondition = {
#             "condition_code": code,
#             "condition_name": condition["condition_name"],
#             "is_hcc": code in hcc_code_set,
#             "condition_data": condition["condition_data"]
#         }
        
#         validated_conditions.append(validated_condition)
    
#     logger.info(f"Validated {len(validated_conditions)} conditions")
    
#     # Count HCC conditions
#     hcc_count = sum(1 for c in validated_conditions if c["is_hcc"])
#     logger.info(f"Found {hcc_count} HCC-relevant conditions")
    
#     # Return updated state
#     return {"conditions": validated_conditions}

# def condition_validator(state: OverallState) -> OverallState:
#     """
#     Validate conditions against HCC-relevant codes.
    
#     Args:
#         state: The current state containing extracted conditions
        
#     Returns:
#         OverallState: Updated state with validated conditions
#     """
#     logger.info("Validating conditions against HCC-relevant codes")
    
#     # Get the raw conditions from state
#     raw_conditions = state.get("raw_conditions", [])
    
#     if not raw_conditions:
#         logger.warning("No conditions to validate")
#         return {"conditions": []}
    
#     # Get HCC codes from input state
#     input_state = state.get("_input", {})
#     hcc_codes = input_state.get("hcc_codes", [])
    
#     # Create set of normalized HCC codes for faster lookup
#     # Normalize by removing dots and converting to uppercase
#     normalized_hcc_code_set = set()
#     for code in hcc_codes:
#         # Normalize the code: remove dots and make uppercase
#         normalized_code = code.replace(".", "").upper()
#         normalized_hcc_code_set.add(normalized_code)
#         # Also add the original code for exact matches
#         normalized_hcc_code_set.add(code.upper())
    
#     # Always use the direct validation approach since it's more reliable
#     validated_conditions: List[ValidatedCondition] = []
    
#     for condition in raw_conditions:
#         code = condition["condition_code"]
        
#         # Normalize the condition code the same way
#         normalized_code = code.replace(".", "").upper()
        
#         # Check both original and normalized code formats
#         is_hcc = (code.upper() in normalized_hcc_code_set) or (normalized_code in normalized_hcc_code_set)
        
#         validated_condition: ValidatedCondition = {
#             "condition_code": code,
#             "condition_name": condition["condition_name"],
#             "is_hcc": is_hcc,
#             "condition_data": condition["condition_data"]
#         }
        
#         validated_conditions.append(validated_condition)
    
#     logger.info(f"Validated {len(validated_conditions)} conditions")
    
#     # Count HCC conditions
#     hcc_count = sum(1 for c in validated_conditions if c["is_hcc"])
#     logger.info(f"Found {hcc_count} HCC-relevant conditions")
    
#     # Return updated state
#     return {"conditions": validated_conditions}

def condition_validator(state: OverallState) -> OverallState:
    """
    Validate conditions against HCC-relevant codes.
    
    Args:
        state: The current state containing extracted conditions
        
    Returns:
        OverallState: Updated state with validated conditions
    """
    logger.info("Validating conditions against HCC-relevant codes")
    
    # Get the raw conditions from state
    raw_conditions = state.get("raw_conditions", [])
    
    if not raw_conditions:
        logger.warning("No conditions to validate")
        return {"conditions": []}
    
    # Get HCC codes from input state
    input_state = state.get("_input", {})
    hcc_codes = input_state.get("hcc_codes", [])
    
    # Get the pre-normalized HCC code set if available
    normalized_hcc_code_set = input_state.get("normalized_hcc_code_set")
    
    # If not available, create it
    if not normalized_hcc_code_set:
        # Create set of normalized HCC codes for faster lookup
        # Normalize by removing dots and converting to uppercase
        normalized_hcc_code_set = set()
        for code in hcc_codes:
            # Normalize the code: remove dots and make uppercase
            normalized_code = code.replace(".", "").upper()
            normalized_hcc_code_set.add(normalized_code)
            # Also add the original code for exact matches
            normalized_hcc_code_set.add(code.upper())
    
    # Log some sample codes for debugging
    if normalized_hcc_code_set:
        sample_codes = list(normalized_hcc_code_set)[:5] if len(normalized_hcc_code_set) > 5 else list(normalized_hcc_code_set)
        logger.info(f"Sample normalized HCC codes in validator: {sample_codes}")
    
    # Always use the direct validation approach since it's more reliable
    validated_conditions: List[ValidatedCondition] = []
    
    for condition in raw_conditions:
        code = condition["condition_code"]
        
        # Normalize the condition code the same way
        normalized_code = code.replace(".", "").upper()
        
        # Check both original and normalized code formats
        original_in_set = code.upper() in normalized_hcc_code_set
        normalized_in_set = normalized_code in normalized_hcc_code_set
        is_hcc = original_in_set or normalized_in_set
        
        # Log each validation for debugging
        logger.info(f"Condition {code} (normalized: {normalized_code}) - HCC status: {is_hcc} (original match: {original_in_set}, normalized match: {normalized_in_set})")
        
        validated_condition: ValidatedCondition = {
            "condition_code": code,
            "condition_name": condition["condition_name"],
            "is_hcc": is_hcc,
            "condition_data": condition["condition_data"]
        }
        
        validated_conditions.append(validated_condition)
    
    logger.info(f"Validated {len(validated_conditions)} conditions")
    
    # Count HCC conditions
    hcc_count = sum(1 for c in validated_conditions if c["is_hcc"])
    logger.info(f"Found {hcc_count} HCC-relevant conditions")
    
    # Return updated state
    return {"conditions": validated_conditions}