"""
Test utilities for parsing progress notes.
"""

import logging
import sys
import os
from pathlib import Path
import re
from typing import Dict, List, Any, Optional

# Add the project root to the path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from packages.framework.document_loaders.note_loader import (
    load_progress_note,
    parse_note_sections,
    extract_assessment_plan,
    extract_condition_blocks
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

# Sample progress note for testing
SAMPLE_NOTE = """
Screening
None recorded.
ROS
ROS as noted in the HPI
Physical Exam
None recorded.
Assessment / Plan

1. Gastroesophageal reflux disease -
   Stable
   Continue the antacids
   F/U in 3 months
   K21.9: Gastro-esophageal reflux disease without esophagitis

2. Hyperglycemia due to type 2 diabetes mellitus -
   Worsening
   Continue Metformin1000 mg BID and Glimepiride 8 mg
   Recommend a low sugar and low carbohydrate diet.
   Discussed 1/2 plate with non-starchy vegetables
   Include healthy fats in your meal like: Olive oil
   E11.65: Type 2 diabetes mellitus with hyperglycemia
"""

def test_progress_note_parser():
    """Test the progress note parser functionality."""
    logger.info("Testing progress note parser")
    
    # Parse the note
    loaded_note = load_progress_note(SAMPLE_NOTE)
    
    # Verify the loaded note
    assert "raw_content" in loaded_note, "Loaded note should contain raw_content"
    assert "sections" in loaded_note, "Loaded note should contain sections"
    assert "assessment_plan" in loaded_note, "Loaded note should contain assessment_plan"
    
    # Verify sections
    sections = loaded_note["sections"]
    assert "Assessment / Plan" in sections, "Sections should include Assessment / Plan"
    
    # Verify assessment plan
    assessment_plan = loaded_note["assessment_plan"]
    assert "Gastroesophageal reflux disease" in assessment_plan, "Assessment plan should include GERD"
    assert "Hyperglycemia due to type 2 diabetes mellitus" in assessment_plan, "Assessment plan should include diabetes"
    
    # Extract condition blocks
    condition_blocks = extract_condition_blocks(assessment_plan)
    assert len(condition_blocks) == 2, "Should extract 2 condition blocks"
    
    # Verify the first condition block
    assert "K21.9" in condition_blocks[0], "First condition should include K21.9 code"
    assert "Gastroesophageal reflux disease" in condition_blocks[0], "First condition should be GERD"
    
    # Verify the second condition block
    assert "E11.65" in condition_blocks[1], "Second condition should include E11.65 code"
    assert "Hyperglycemia due to type 2 diabetes mellitus" in condition_blocks[1], "Second condition should be diabetes"
    
    logger.info("Progress note parser test completed successfully")
    
    return loaded_note, condition_blocks

if __name__ == "__main__":
    test_progress_note_parser()