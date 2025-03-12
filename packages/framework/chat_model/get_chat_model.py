"""
Function to get a chat model based on the specified model name.
"""

import os
from typing import Literal, Dict, Any, Optional
from langchain.chat_models.base import BaseChatModel
from langchain_google_vertexai import ChatVertexAI
from langchain_google_vertexai import HarmBlockThreshold, HarmCategory

# Define Literal for model values
ModelType = Literal[
    "gemini-1.5-flash",
    "gemini-1.5-flash-001",
    "gemini-1.5-flash-002",
    "gemini-1.5-pro",
    "gemini-1.5-pro-001",
    "gemini-1.5-pro-002",
]

# Map model names to their corresponding classes
modelToClassMap = {
    "gemini-1.5-flash": ChatVertexAI,
    "gemini-1.5-flash-001": ChatVertexAI,
    "gemini-1.5-flash-002": ChatVertexAI,
    "gemini-1.5-pro": ChatVertexAI,
    "gemini-1.5-pro-001": ChatVertexAI,
    "gemini-1.5-pro-002": ChatVertexAI,
}


def get_chat_model(
    model_name: ModelType = None,
    temperature: Optional[float] = 0,
    max_tokens: Optional[int] = None,
    max_retries: Optional[int] = 6,
    stop: Optional[str] = None,
    safety_settings: Optional[Dict[HarmCategory, HarmBlockThreshold]] = None,
    **extra_props: Any,
) -> BaseChatModel:
    """
    Get a chat model based on the specified model name.
    
    Args:
        model_name: Name of the model to use
        temperature: Temperature for the model
        max_tokens: Maximum tokens for the model
        max_retries: Maximum number of retries
        stop: Stop sequence
        safety_settings: Safety settings for the model
        extra_props: Additional properties for the model
        
    Returns:
        BaseChatModel: Configured chat model
    """
    # Use environment variable for model name if not provided
    if model_name is None:
        model_name = os.getenv("MODEL_NAME", "gemini-1.5-flash")
    
    # Default safety settings to turn off content filtering
    if safety_settings is None:
        safety_settings = {
            HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        }
    
    # Base configuration for all models
    base_config = {
        "temperature": temperature,
        "max_tokens": max_tokens,
        "max_retries": max_retries,
        "stop": stop,
    }
    
    # Get Google project ID from environment
    project_id = os.getenv("GOOGLE_PROJECT_ID")
    if project_id:
        base_config["project"] = project_id

    # Include safety_settings for Gemini models
    if model_name.startswith("gemini-"):
        base_config["safety_settings"] = safety_settings

    # Merge base_config with extra_props
    full_config = {**base_config, **extra_props}

    # Check if we can create the model
    if model_name not in modelToClassMap:
        raise ValueError(f"Unsupported model: {model_name}")
        
    ChatClass = modelToClassMap[model_name]

    # Configure the specified model
    return ChatClass(model_name=model_name, **full_config)