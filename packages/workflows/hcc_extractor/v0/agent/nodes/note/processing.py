# """
# Node for processing progress notes and extracting condition blocks.
# """

# import logging
# import re
# from typing import List

# from packages.workflows.hcc_extractor.v0.agent.schemas.states import OverallState
# from packages.workflows.hcc_extractor.v0.agent.schemas.format_instructions import ProcessedNote
# from packages.workflows.hcc_extractor.v0.agent.prompt_templates import note_processing_prompt
# from packages.workflows.hcc_extractor.v0.utils.call_llm import call_llm
# from packages.framework.document_loaders.note_loader import extract_condition_blocks

# logger = logging.getLogger(__name__)

# def note_processor(state: OverallState) -> OverallState:
#     """
#     Process the progress note to identify condition blocks.
    
#     Args:
#         state: The current state containing the loaded note
        
#     Returns:
#         OverallState: Updated state with condition blocks
#     """
#     logger.info("Processing progress note to extract condition blocks")
    
#     # Get the note from state
#     note = state["note"]
#     raw_content = note["raw_content"]
#     assessment_plan = note["assessment_plan"]
    
#     # If assessment_plan is already extracted, use it
#     if assessment_plan:
#         logger.info("Using already extracted Assessment/Plan section")
#         has_assessment_plan = True
#     else:
#         # Process the note with LLM to identify Assessment/Plan section
#         logger.info("Using LLM to identify Assessment/Plan section")
#         processed: ProcessedNote = call_llm(
#             prompt_template=note_processing_prompt,
#             input_parameters={"note_content": raw_content},
#             pydantic_object=ProcessedNote
#         )
        
#         assessment_plan = processed.assessment_plan_content
#         has_assessment_plan = processed.has_assessment_plan
        
#         if not has_assessment_plan:
#             logger.warning("No Assessment/Plan section found in the note")
    
#     # Extract condition blocks from the assessment plan
#     if has_assessment_plan and assessment_plan:
#         # First try with regex-based extraction
#         condition_blocks = extract_condition_blocks(assessment_plan)
        
#         # If no blocks found, use the ones from LLM processing if available
#         if not condition_blocks and "processed" in locals():
#             condition_blocks = processed.condition_blocks
#     else:
#         condition_blocks = []
    
#     # Update the note in the state
#     note["assessment_plan"] = assessment_plan
#     note["condition_blocks"] = condition_blocks
    
#     logger.info(f"Extracted {len(condition_blocks)} condition blocks")
    
#     # Return updated state
#     return {"note": note}


# v1
"""
Node for processing progress notes and extracting condition blocks.
"""

import logging
import re
from typing import List

from packages.workflows.hcc_extractor.v0.agent.schemas.states import OverallState
from packages.workflows.hcc_extractor.v0.agent.schemas.format_instructions import ProcessedNote
from packages.workflows.hcc_extractor.v0.agent.prompt_templates import note_processing_prompt
from packages.workflows.hcc_extractor.v0.utils.call_llm import call_llm
from packages.framework.document_loaders.note_loader import extract_condition_blocks

logger = logging.getLogger(__name__)

def note_processor(state: OverallState) -> OverallState:
    """
    Process the progress note to identify condition blocks.
    
    Args:
        state: The current state containing the loaded note
        
    Returns:
        OverallState: Updated state with condition blocks
    """
    logger.info("Processing progress note to extract condition blocks")
    
    # Get the note from state
    note = state["note"]
    raw_content = note["raw_content"]
    assessment_plan = note["assessment_plan"]
    
    # If assessment_plan is already extracted, use it
    if assessment_plan:
        logger.info("Using already extracted Assessment/Plan section")
        has_assessment_plan = True
    else:
        # Process the note with LLM to identify Assessment/Plan section
        logger.info("Using LLM to identify Assessment/Plan section")
        processed: ProcessedNote = call_llm(
            prompt_template=note_processing_prompt,
            input_parameters={"note_content": raw_content},
            pydantic_object=ProcessedNote
        )
        
        assessment_plan = processed.assessment_plan_content
        has_assessment_plan = processed.has_assessment_plan
        
        if not has_assessment_plan:
            logger.warning("No Assessment/Plan section found in the note")
    
    # Extract condition blocks from the assessment plan
    if has_assessment_plan and assessment_plan:
        # First try with regex-based extraction
        condition_blocks = extract_condition_blocks(assessment_plan)
        
        # If no blocks found, use the ones from LLM processing if available
        if not condition_blocks and "processed" in locals():
            condition_blocks = processed.condition_blocks
            
        # If still no blocks found, use the assessment plan as a single block
        if not condition_blocks:
            logger.warning("No structured condition blocks found, using entire assessment plan as a single block")
            condition_blocks = [assessment_plan]
    else:
        condition_blocks = []
        
    # Log the extracted blocks for debugging
    logger.info(f"Extracted {len(condition_blocks)} condition blocks")
    for i, block in enumerate(condition_blocks):
        logger.debug(f"Block {i+1}: {block[:100]}...")
    
    # Update the note in the state
    note["assessment_plan"] = assessment_plan
    note["condition_blocks"] = condition_blocks
    
    logger.info(f"Extracted {len(condition_blocks)} condition blocks")
    
    # Return updated state
    return {"note": note}