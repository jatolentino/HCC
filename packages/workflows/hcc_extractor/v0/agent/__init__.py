"""
LangGraph agent for HCC condition extraction.
"""

from langgraph.graph import StateGraph, START, END

from packages.workflows.hcc_extractor.v0.agent.nodes.note.loading import note_loader
from packages.workflows.hcc_extractor.v0.agent.nodes.note.processing import note_processor
from packages.workflows.hcc_extractor.v0.agent.nodes.condition.extraction import condition_extractor
from packages.workflows.hcc_extractor.v0.agent.nodes.condition.validation import condition_validator
from packages.workflows.hcc_extractor.v0.agent.nodes.condition.output import output_formatter
from packages.workflows.hcc_extractor.v0.agent.schemas.states import OverallState, InputState

# Define the graph
builder = StateGraph(OverallState, input=InputState)

# Add nodes
builder.add_node("note_loader", note_loader)
builder.add_node("note_processor", note_processor)
builder.add_node("condition_extractor", condition_extractor)
builder.add_node("condition_validator", condition_validator)
builder.add_node("output_formatter", output_formatter)

# Add edges
builder.add_edge(START, "note_loader")
builder.add_edge("note_loader", "note_processor")
builder.add_edge("note_processor", "condition_extractor")
builder.add_edge("condition_extractor", "condition_validator")
builder.add_edge("condition_validator", "output_formatter")
builder.add_edge("output_formatter", END)

# Compile the graph
hcc_extraction_agent = builder.compile()