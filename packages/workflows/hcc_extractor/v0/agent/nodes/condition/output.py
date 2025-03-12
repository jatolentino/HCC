"""
Node for formatting output conditions.
"""

import logging
from typing import List, Dict, Any

from packages.workflows.hcc_extractor.v0.agent.schemas.states import OverallState, ValidatedCondition

logger = logging.getLogger(__name__)

def output_formatter(state: OverallState) -> OverallState:
    """
    Format the validated conditions for output.
    
    Args:
        state: The current state containing validated conditions
        
    Returns:
        OverallState: Final state with formatted output
    """
    logger.info("Formatting conditions for output")
    
    # Get validated conditions from state
    conditions = state.get("conditions", [])
    
    # No formatting needed for now, just return the conditions as is
    # This node can be expanded for additional output formatting if needed
    
    logger.info(f"Formatted {len(conditions)} conditions for output")
    
    # Return formatted conditions
    return {"conditions": conditions}