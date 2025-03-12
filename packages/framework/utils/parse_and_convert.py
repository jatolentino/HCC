"""
Utility function for parsing and converting Pydantic models.
"""

from typing import Any, Dict

def parse_and_convert(result: Any) -> Dict:
    """
    Convert a Pydantic model to a dictionary.
    
    Args:
        result: Pydantic model instance
        
    Returns:
        Dict: Dictionary representation of the model
    """
    if hasattr(result, "model_dump"):
        return result.model_dump()
    elif hasattr(result, "dict"):
        return result.dict()
    return result