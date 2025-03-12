"""
Schemas for condition data structures.
"""

from typing import List, Dict, Any, Optional, TypedDict
from pydantic import BaseModel, Field

class Condition(BaseModel):
    """Pydantic model for a medical condition."""
    condition_code: str = Field(description="ICD-10 code for the condition")
    condition_name: str = Field(description="Name of the condition")
    is_hcc: bool = Field(description="Whether the condition is HCC-relevant")
    condition_data: str = Field(description="Clinical data about the condition")

class ConditionDict(TypedDict):
    """TypedDict for a medical condition."""
    condition_code: str
    condition_name: str
    is_hcc: bool
    condition_data: str

class ProgressNoteInput(BaseModel):
    """Input schema for progress note processing."""
    note_content: str = Field(description="Content of the progress note")

class ExtractedConditions(BaseModel):
    """Output schema for extracted conditions."""
    conditions: List[Condition] = Field(description="List of extracted conditions")