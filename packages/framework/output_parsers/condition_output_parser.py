"""
Output parser for extracting conditions from LLM responses.
"""

import re
import json
from typing import List, Dict, Any, Union
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator

class ExtractedCondition(BaseModel):
    """Schema for an extracted medical condition."""
    condition_code: str = Field(description="ICD-10 code for the condition")
    condition_name: str = Field(description="Name of the condition")
    condition_data: str = Field(description="Clinical data about the condition")
    
    @validator("condition_code")
    def validate_code_format(cls, v):
        """Validate that the code is in the correct format."""
        # ICD-10 codes typically start with a letter followed by digits
        if not re.match(r"^[A-Z]\d+\.?\d*$", v):
            raise ValueError(f"Invalid ICD-10 code format: {v}")
        return v

class ExtractedConditions(BaseModel):
    """Schema for multiple extracted conditions."""
    conditions: List[ExtractedCondition] = Field(description="List of extracted conditions")

class ConditionOutputParser:
    """Parser for extracting conditions from LLM outputs."""
    
    @staticmethod
    def parse(text: str) -> List[Dict[str, Any]]:
        """
        Parse raw text output from an LLM into structured condition data.
        
        Args:
            text: Raw text output from LLM
            
        Returns:
            List[Dict[str, Any]]: List of condition dictionaries
        """
        # First try to parse as JSON
        try:
            # Check if the text contains a JSON array
            match = re.search(r'\[.*\]', text, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
                
                # Validate that each item has the required fields
                for item in data:
                    if not all(k in item for k in ["condition_code", "condition_name", "condition_data"]):
                        raise ValueError("Missing required fields in JSON output")
                
                return data
        except (json.JSONDecodeError, ValueError):
            pass
        
        # If JSON parsing fails, try to extract structured data from text
        conditions = []
        
        # Look for patterns like "Code: X00.0 - Name: Condition Name"
        code_pattern = r"(?:Code|ICD-10|Condition Code):\s*([A-Z]\d+\.?\d*)"
        name_pattern = r"(?:Name|Condition|Condition Name):\s*([^\n]+)"
        data_pattern = r"(?:Data|Details|Plan|Condition Data):\s*([^\n]+(?:\n[^\n]+)*)"
        
        # Find all codes
        codes = re.findall(code_pattern, text)
        
        # For each code, try to find the corresponding name and data
        for i, code in enumerate(codes):
            name_match = re.search(name_pattern, text)
            data_match = re.search(data_pattern, text)
            
            name = name_match.group(1).strip() if name_match else f"Condition {i+1}"
            data = data_match.group(1).strip() if data_match else ""
            
            conditions.append({
                "condition_code": code,
                "condition_name": name,
                "condition_data": data
            })
        
        return conditions

class ConditionPydanticParser:
    """Pydantic-based parser for conditions."""
    
    def __init__(self):
        self.parser = PydanticOutputParser(pydantic_object=ExtractedConditions)
    
    def get_format_instructions(self) -> str:
        """
        Get format instructions for the LLM.
        
        Returns:
            str: Format instructions
        """
        return self.parser.get_format_instructions()
    
    def parse(self, text: str) -> List[Dict[str, Any]]:
        """
        Parse text using Pydantic parser.
        
        Args:
            text: Text to parse
            
        Returns:
            List[Dict[str, Any]]: Parsed conditions
        """
        try:
            parsed = self.parser.parse(text)
            return [condition.dict() for condition in parsed.conditions]
        except Exception as e:
            # Fallback to the simpler parser
            return ConditionOutputParser.parse(text)