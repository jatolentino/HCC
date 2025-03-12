"""
Node for loading and initial processing of progress notes.
"""

import logging
from packages.workflows.hcc_extractor.v0.agent.schemas.states import InputState, OverallState, ProgressNote
from packages.framework.document_loaders.note_loader import load_progress_note

logger = logging.getLogger(__name__)

def note_loader(state: InputState) -> OverallState:
    """
    Load and preprocess a clinical progress note.
    
    Args:
        state: The input state containing the note content
        
    Returns:
        OverallState: Updated state with the loaded note
    """
    logger.info("Loading progress note")
    
    # Get note content from state
    note_content = state["note_content"]
    
    # Load and preprocess the note
    note_data = load_progress_note(note_content)
    
    # Initialize the progress note state
    progress_note: ProgressNote = {
        "raw_content": note_content,
        "assessment_plan": note_data.get("assessment_plan", ""),
        "condition_blocks": []  # Will be populated in the next step
    }
    
    # Return updated state
    return {
        "note": progress_note
    }