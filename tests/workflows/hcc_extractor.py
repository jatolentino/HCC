"""
Test for the HCC extractor workflow.
"""

import logging
import sys
import os
from pathlib import Path
import json

# Add the project root to the path
sys.path.append(str(Path(__file__).parent.parent.parent))

from packages.workflows.hcc_extractor.v0 import run_hcc_extractor_v0

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

def test_hcc_extractor():
    """Test the HCC extractor with a sample progress note."""
    logger.info("Starting HCC extractor test")
    
    # Create a results directory
    results_dir = Path("tests/results")
    results_dir.mkdir(exist_ok=True, parents=True)
    
    try:
        # Run the extractor
        result = run_hcc_extractor_v0(note_content=SAMPLE_NOTE)
        
        # Log the result
        logger.info(f"Extraction result: {json.dumps(result, indent=2)}")
        
        # Save the result to a file
        output_path = results_dir / "test_result.json"
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)
        
        logger.info(f"Test result saved to {output_path}")
        
        # Verify the result
        assert isinstance(result, list), "Result should be a list"
        assert len(result) > 0, "At least one condition should be extracted"
        
        for condition in result:
            assert "condition_code" in condition, "Each condition should have a code"
            assert "condition_name" in condition, "Each condition should have a name"
            assert "is_hcc" in condition, "Each condition should have HCC relevance"
            assert "condition_data" in condition, "Each condition should have data"
        
        logger.info("HCC extractor test completed successfully")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_hcc_extractor()