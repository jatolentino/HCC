from typing import Dict, Any, TypedDict
import json
import os
from langgraph.graph import END, StateGraph
from langchain_google_vertexai import VertexAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

PROJECT_ID = os.getenv('PROJECT_ID')
LOCATION = os.getenv('LOCATION')
CREDENTIALS_PATH = os.getenv('CREDENTIALS_PATH')

# Define the state schema for the graph
class GraphState(TypedDict):
    assessment_plan: str
    extracted_text: str | None
    condition_data: str | None

# Function to initialize Vertex AI with proper authentication
def initialize_vertex_model(project_id=None, location=None, credentials_path=None):
    """Initialize Vertex AI model with proper authentication."""
    # Set environment variables if credentials path is provided
    if credentials_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

    # Initialize Vertex AI model with explicit project and location
    return VertexAI(
        model_name="gemini-pro",
        project=project_id,  # Pass your GCP project ID
        location=location or "us-central1",  # Default region
        temperature=0
    )

# Define extraction prompt
extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert medical data processor. Your task is to extract relevant condition management details from the assessment plan.
    
Extract ONLY information that refers to:
1. Medications or treatment regimens
2. Patient counseling or education 
3. Direct management instructions
4. Diagnostic or testing plans
5. Referral information

Do NOT include:
- Diagnostic codes (like ICD-10 codes such as K21.9, J44.9)
- Status descriptions (like "Unchanged", "Stable", "Worsening")
- Vital signs or lab values (like SPO2-98%)
- Assessment headings or condition names (like "GERD", "Chronic obstructive lung disease")

Return ONLY the extracted information, exactly as written in the original text, with each item on a new line.
If no relevant management information is found, return an empty string."""),
    ("human", "Here is the assessment plan text:\n\n{assessment_plan}")
])

# Function to extract condition data using Vertex AI
def extract_condition_data(state: GraphState) -> GraphState:
    """Extract condition data from assessment plan using LLM"""
    assessment_plan = state["assessment_plan"]

    try:
        # Initialize real Vertex AI model
        model = initialize_vertex_model(
            project_id = PROJECT_ID,
            location = LOCATION,
            credentials_path = CREDENTIALS_PATH
        )

        # Create and run extraction chain
        extraction_chain = extraction_prompt | model | StrOutputParser()
        extracted_text = extraction_chain.invoke({"assessment_plan": assessment_plan})

        return {**state, "extracted_text": extracted_text}
    except Exception as e:
        print(f"Error using LLM for extraction: {e}")
        # Return empty extraction if both real and mock LLM fail
        return {**state, "extracted_text": ""}

# Function to format the extracted text as proper JSON
def format_as_json(state: GraphState) -> GraphState:
    """Format the extracted text as JSON"""
    if not state.get("extracted_text"):
        return {**state, "condition_data": "[]"}

    extracted_lines = state["extracted_text"].strip().split("\n")
    # Filter out any empty lines
    extracted_lines = [line for line in extracted_lines if line.strip()]

    return {**state, "condition_data": json.dumps(extracted_lines, indent=2)}

# Create the graph
def create_graph():
    # Define the state graph with schema
    workflow = StateGraph(GraphState)

    # Add nodes to the graph
    workflow.add_node("extract_condition_data", extract_condition_data)
    workflow.add_node("format_json", format_as_json)

    # Define graph edges
    workflow.add_edge("extract_condition_data", "format_json")
    workflow.add_edge("format_json", END)

    # Set entry point
    workflow.set_entry_point("extract_condition_data")

    return workflow.compile()

# Main pipeline function to process the assessment plan
def process_assessment_plan(assessment_plan: str) -> Dict[str, Any]:
    # Initialize the graph
    graph = create_graph()

    # Run the graph with the assessment plan
    config = {"recursion_limit": 25}
    result = graph.invoke({"assessment_plan": assessment_plan}, config=config)

    return result

# Example usage
if __name__ == "__main__":
    # Example 1: COPD case
    sample_input1 = """3. Chronic obstructive lung disease -
Unchanged
SPO2-98% today
Maintain current inhaler regimen: Tiotropium and Fluticasone/Salmeterol.
Counseled for smoking cessation today
J44.9: Chronic obstructive pulmonary disease, unspecified"""

    # Example 2: GERD case
    sample_input2 = """3) GERD -  K21.9
- Worsening
- Will order EGD and GI consult"""

    # Process both examples
    for idx, sample in enumerate([sample_input1, sample_input2], 1):
        #print(f"\nExample {idx}:")
        #print(f"Input Assessment Plan:\n{sample}\n")

        result = process_assessment_plan(sample)
        print(f"Extracted Condition Data:\n{result['condition_data']}")