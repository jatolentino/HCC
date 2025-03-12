#!/usr/bin/env python3
"""
Main entry point for the Clinical HCC Extractor application.
This app processes clinical progress notes, extracts conditions,
and determines if they are HCC-relevant.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the project root to the path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

# Check if we're in fallback mode
use_fallback = os.getenv("USE_FALLBACK_EXTRACTION", "").lower() in ("true", "1", "yes")

# Only check credentials if not in fallback mode
if not use_fallback:
    # Verify Google credentials are available before importing vertex-dependent modules
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path and not os.path.exists(credentials_path):
        logger.error(f"Google credentials file not found at: {credentials_path}")
        logger.error("Please ensure the service-account.json file is mounted correctly in the container")
        logger.error("Example: docker run -v /path/to/credentials:/app/credentials clinical-hcc-extractor")
        logger.error("Alternatively, run with USE_FALLBACK_EXTRACTION=true to use regex-based extraction")
        sys.exit(1)

# Import required modules
try:
    # First import the run_hcc_extractor_v0 function directly
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
        from packages.workflows.hcc_extractor.v0 import run_hcc_extractor_v0
    except ImportError as ie:
        logger.error(f"Failed to import modules: {str(ie)}")
        logger.error("Trying alternative import method...")
        # If direct import fails, try the alternative approach
        from packages.workflows import run_hcc_extractor_v0
    
    from apps.hcc_extractor_app.methods.process_run import process_progress_notes
except Exception as e:
    logger.error(f"Error importing modules: {str(e)}")
    logger.error("This is likely due to missing or invalid Google credentials")
    logger.error("Run with USE_FALLBACK_EXTRACTION=true to use regex-based extraction")
    sys.exit(1)

def main():
    """Main function to run the HCC extractor application."""
    logger.info("Starting Clinical HCC Extractor")
    
    # Get output directory from environment or use default
    output_dir = os.getenv("OUTPUT_DIR", "results")
    os.makedirs(output_dir, exist_ok=True)
    
    # Check for Google Project ID if not in fallback mode
    if not use_fallback:
        project_id = os.getenv("GOOGLE_PROJECT_ID")
        if not project_id:
            logger.warning("GOOGLE_PROJECT_ID not set. This may cause authentication issues.")
            logger.warning("Set this when building the Docker image with --build-arg GOOGLE_PROJECT_ID=your-project-id")
            logger.warning("Alternatively, run with USE_FALLBACK_EXTRACTION=true to use regex-based extraction")
    else:
        logger.info("Running in fallback mode (LLM-free extraction)")
        
    # Process all progress notes
    try:
        results = process_progress_notes(run_hcc_extractor_v0)
        
        # Print results
        for note_filename, conditions in results.items():
            logger.info(f"Results for {note_filename}:")
            formatted_json = json.dumps(conditions, indent=2)
            logger.info(formatted_json)
            
            # Save results to output directory
            output_path = Path(output_dir) / f"{note_filename}_results.json"
            with open(output_path, "w") as f:
                f.write(formatted_json)
            logger.info(f"Results saved to {output_path}")
        
        logger.info("HCC extraction completed successfully")
    except Exception as e:
        logger.error(f"Error in HCC extraction process: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()