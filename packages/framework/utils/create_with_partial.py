"""
Utility function for creating prompt templates with partial parameters.
"""

from typing import Any, Callable

def create_with_partial(
    **params: Any,
) -> Callable[..., Any]:
    """
    Create a wrapper function that applies partial parameters to a prompt template.
    
    Args:
        **params: Parameters to partially apply to the template
        
    Returns:
        Callable: A wrapper function
    """
    def wrapper(template, **extra_params):
        merged_params = {
            **{key: str(value) for key, value in params.items()},
            **{key: str(value) for key, value in extra_params.items()},
        }
        return template.partial(**merged_params)

    return wrapper