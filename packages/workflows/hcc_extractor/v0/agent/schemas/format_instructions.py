# """
# Pydantic models for LLM response format instructions.
# """

# from typing import List, Dict, Any, Optional
# from pydantic import BaseModel, Field

# class ExtractedCondition(BaseModel):
#     """Schema for an extracted medical condition."""
#     condition_code: str = Field(description="ICD-10 code for the condition")
#     condition_name: str = Field(description="Name of the condition")
#     condition_data: str = Field(description="Clinical data about the condition")

# class ExtractedConditions(BaseModel):
#     """Schema for multiple extracted conditions."""
#     conditions: List[ExtractedCondition] = Field(description="List of extracted conditions")

# class ProcessedNote(BaseModel):
#     """Schema for a processed progress note."""
#     has_assessment_plan: bool = Field(description="Whether the note contains an Assessment/Plan section")
#     assessment_plan_content: str = Field(description="Content of the Assessment/Plan section")
#     condition_blocks: List[str] = Field(description="List of identified condition blocks")
    
# class ValidatedCondition(BaseModel):
#     """Schema for a validated medical condition."""
#     condition_code: str = Field(description="ICD-10 code for the condition")
#     condition_name: str = Field(description="Name of the condition")
#     is_hcc: bool = Field(description="Whether the condition is HCC-relevant")
#     condition_data: str = Field(description="Clinical data about the condition")


# v1
"""
Pydantic models for LLM response format instructions.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ExtractedCondition(BaseModel):
    """Schema for an extracted medical condition."""
    condition_code: str = Field(description="ICD-10 code for the condition")
    condition_name: str = Field(description="Name of the condition")
    condition_data: str = Field(description="Clinical data about the condition")

class ExtractedConditions(BaseModel):
    """Schema for multiple extracted conditions."""
    conditions: List[ExtractedCondition] = Field(default_factory=list, description="List of extracted conditions")

class ProcessedNote(BaseModel):
    """Schema for a processed progress note."""
    has_assessment_plan: bool = Field(default=False, description="Whether the note contains an Assessment/Plan section")
    assessment_plan_content: str = Field(default="", description="Content of the Assessment/Plan section")
    condition_blocks: List[str] = Field(default_factory=list, description="List of identified condition blocks")
    
class ValidatedCondition(BaseModel):
    """Schema for a validated medical condition."""
    condition_code: str = Field(description="ICD-10 code for the condition")
    condition_name: str = Field(description="Name of the condition")
    is_hcc: bool = Field(default=False, description="Whether the condition is HCC-relevant")
    condition_data: str = Field(description="Clinical data about the condition")