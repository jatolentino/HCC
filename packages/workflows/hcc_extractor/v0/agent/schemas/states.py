"""
State definitions for the HCC extraction agent.
"""

from typing import List, Dict, Any, Optional, TypedDict
from typing_extensions import Annotated, NotRequired
import operator

class InputState(TypedDict):
    """Input state for the HCC extraction agent."""
    note_content: str
    hcc_codes: List[str]

class ProgressNote(TypedDict):
    """Progress note representation."""
    raw_content: str
    assessment_plan: str
    condition_blocks: List[str]

class Condition(TypedDict):
    """Extracted condition."""
    condition_code: str
    condition_name: str
    condition_data: str

class ValidatedCondition(TypedDict):
    """Validated condition with HCC relevance."""
    condition_code: str
    condition_name: str
    is_hcc: bool
    condition_data: str

# Define a merge function for conditions
def merge_conditions(
    existing_conditions: List[ValidatedCondition], 
    new_conditions: List[ValidatedCondition]
) -> List[ValidatedCondition]:
    """
    Merge new conditions with existing conditions.
    
    Args:
        existing_conditions: List of existing conditions
        new_conditions: List of new conditions
        
    Returns:
        List[ValidatedCondition]: Merged list
    """
    # Create a dictionary of existing conditions by code
    conditions_dict = {c["condition_code"]: c for c in existing_conditions}
    
    # Add new conditions
    for condition in new_conditions:
        code = condition["condition_code"]
        if code in conditions_dict:
            # Update existing condition if needed
            if condition.get("condition_name") and not conditions_dict[code].get("condition_name"):
                conditions_dict[code]["condition_name"] = condition["condition_name"]
            
            if condition.get("condition_data") and not conditions_dict[code].get("condition_data"):
                conditions_dict[code]["condition_data"] = condition["condition_data"]
        else:
            # Add new condition
            conditions_dict[code] = condition
    
    # Convert back to list
    return list(conditions_dict.values())

class OverallState(TypedDict):
    """Overall state of the HCC extraction agent."""
    note: NotRequired[ProgressNote]
    raw_conditions: NotRequired[List[Condition]]
    conditions: Annotated[List[ValidatedCondition], merge_conditions]