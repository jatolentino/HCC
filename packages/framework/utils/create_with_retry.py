"""
Utility function for creating chains with retry functionality.
"""

from typing import Optional, Callable, cast
from langchain.prompts import ChatPromptTemplate

def create_with_retry(
    retry: Optional[int] = 3,
) -> Callable[[ChatPromptTemplate], ChatPromptTemplate]:
    """
    Create a decorator function that adds retry functionality to a chat prompt template.
    
    Args:
        retry: Number of retry attempts
        
    Returns:
        Callable: A decorator function
    """
    return lambda template: cast(
        ChatPromptTemplate,
        template.with_retry(stop_after_attempt=retry if retry is not None else 3),
    )