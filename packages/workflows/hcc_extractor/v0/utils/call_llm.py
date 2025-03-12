# """
# Utility for calling LLMs with error handling and retries.
# """

# import logging
# import os
# from typing import Dict, Optional, Any, TypeVar, Type

# from langchain.prompts import ChatPromptTemplate
# from packages.framework.chat_model.get_chat_model import get_chat_model
# from packages.framework.utils.with_retries import with_retries

# logger = logging.getLogger(__name__)

# # Get model parameters from environment
# MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")
# TEMPERATURE = float(os.getenv("TEMPERATURE", "0.1"))
# MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2048"))
# MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

# # Get the model
# LLM = get_chat_model(
#     model_name=MODEL_NAME,
#     temperature=TEMPERATURE,
#     max_tokens=MAX_TOKENS,
#     max_retries=MAX_RETRIES
# )

# T = TypeVar('T')

# @with_retries(max_retries=MAX_RETRIES)
# def call_llm(
#     prompt_template: ChatPromptTemplate,
#     input_parameters: Optional[Dict[str, Any]] = None,
#     pydantic_object: Optional[Type[T]] = None
# ) -> Any:
#     """
#     Call an LLM with the given prompt and parameters.
    
#     Args:
#         prompt_template: The prompt template to use
#         input_parameters: Parameters for the prompt
#         pydantic_object: Optional Pydantic class for parsing the response
        
#     Returns:
#         Any: The LLM response, parsed if pydantic_object is provided
#     """
#     from packages.framework.utils.generic_chain import create_generic_chain
    
#     logger.debug(f"Calling LLM with template: {prompt_template}")
    
#     # Default empty parameters
#     params = input_parameters or {}
    
#     # Create the chain
#     chain = create_generic_chain(
#         chat_model=LLM,
#         template=prompt_template.template,
#         pydantic_class=pydantic_object,
#         **params
#     )
    
#     # Execute the chain
#     result = chain.invoke({})
    
#     # Return the result
#     return result


# v1 call_llm.py
# """
# Utility for calling LLMs with error handling and retries.
# """

# import logging
# import os
# from typing import Dict, Optional, Any, TypeVar, Type

# from langchain.prompts import ChatPromptTemplate
# from packages.framework.chat_model.get_chat_model import get_chat_model
# from packages.framework.utils.with_retries import with_retries

# logger = logging.getLogger(__name__)

# # Get model parameters from environment
# MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")
# TEMPERATURE = float(os.getenv("TEMPERATURE", "0.1"))
# MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2048"))
# MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

# # Get the model - lazy initialization to allow credential checks first
# LLM = None

# def get_llm():
#     """Get the LLM, initializing it if needed."""
#     global LLM
#     if LLM is None:
#         try:
#             LLM = get_chat_model(
#                 model_name=MODEL_NAME,
#                 temperature=TEMPERATURE,
#                 max_tokens=MAX_TOKENS,
#                 max_retries=MAX_RETRIES
#             )
#         except Exception as e:
#             logger.error(f"Failed to initialize LLM: {str(e)}")
#             raise
#     return LLM

# T = TypeVar('T')

# @with_retries(max_retries=MAX_RETRIES)
# def call_llm(
#     prompt_template: ChatPromptTemplate,
#     input_parameters: Optional[Dict[str, Any]] = None,
#     pydantic_object: Optional[Type[T]] = None
# ) -> Any:
#     """
#     Call an LLM with the given prompt and parameters.
    
#     Args:
#         prompt_template: The prompt template to use
#         input_parameters: Parameters for the prompt
#         pydantic_object: Optional Pydantic class for parsing the response
        
#     Returns:
#         Any: The LLM response, parsed if pydantic_object is provided
#     """
#     from packages.framework.utils.generic_chain import create_generic_chain
    
#     logger.debug(f"Calling LLM with template: {prompt_template}")
    
#     # Default empty parameters
#     params = input_parameters or {}
    
#     try:
#         # Get the model and create the chain
#         model = get_llm()
#         chain = create_generic_chain(
#             chat_model=model,
#             template=prompt_template.template,
#             pydantic_class=pydantic_object,
#             **params
#         )
        
#         # Execute the chain
#         result = chain.invoke({})
        
#         # Return the result
#         return result
#     except Exception as e:
#         logger.error(f"Error calling LLM: {str(e)}")
#         # If we're expecting a Pydantic object, return a default instance
#         if pydantic_object:
#             logger.info("Returning default Pydantic object due to LLM error")
#             return pydantic_object.model_construct()
#         raise

# v2
# """
# Utility for calling LLMs with error handling and retries.
# """

# import logging
# import os
# from typing import Dict, Optional, Any, TypeVar, Type

# from langchain.prompts import ChatPromptTemplate
# from packages.framework.chat_model.get_chat_model import get_chat_model
# from packages.framework.utils.with_retries import with_retries

# logger = logging.getLogger(__name__)

# # Get model parameters from environment
# MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")
# TEMPERATURE = float(os.getenv("TEMPERATURE", "0.1"))
# MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2048"))
# MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

# # Get the model - lazy initialization to allow credential checks first
# LLM = None

# def get_llm():
#     """Get the LLM, initializing it if needed."""
#     global LLM
#     if LLM is None:
#         try:
#             LLM = get_chat_model(
#                 model_name=MODEL_NAME,
#                 temperature=TEMPERATURE,
#                 max_tokens=MAX_TOKENS,
#                 max_retries=MAX_RETRIES
#             )
#         except Exception as e:
#             logger.error(f"Failed to initialize LLM: {str(e)}")
#             raise
#     return LLM

# T = TypeVar('T')

# @with_retries(max_retries=MAX_RETRIES)
# def call_llm(
#     prompt_template: ChatPromptTemplate,
#     input_parameters: Optional[Dict[str, Any]] = None,
#     pydantic_object: Optional[Type[T]] = None
# ) -> Any:
#     """
#     Call an LLM with the given prompt and parameters.
    
#     Args:
#         prompt_template: The prompt template to use
#         input_parameters: Parameters for the prompt
#         pydantic_object: Optional Pydantic class for parsing the response
        
#     Returns:
#         Any: The LLM response, parsed if pydantic_object is provided
#     """
#     from packages.framework.utils.generic_chain import create_generic_chain
    
#     logger.debug(f"Calling LLM with template: {prompt_template}")
    
#     # Default empty parameters
#     params = input_parameters or {}
    
#     try:
#         # Get the model and create the chain
#         model = get_llm()
#         chain = create_generic_chain(
#             chat_model=model,
#             template=prompt_template.template,
#             pydantic_class=pydantic_object,
#             **params
#         )
        
#         # Execute the chain
#         result = chain.invoke({})
        
#         # Return the result
#         return result
#     except Exception as e:
#         logger.error(f"Error calling LLM: {str(e)}")
#         # If we're expecting a Pydantic object, return a default instance
#         if pydantic_object:
#             logger.info("Returning default Pydantic object due to LLM error")
#             # Create a default instance with required fields
#             if hasattr(pydantic_object, 'model_construct'):
#                 # For ExtractedConditions, explicitly create with empty conditions list
#                 if pydantic_object.__name__ == 'ExtractedConditions':
#                     return pydantic_object(conditions=[])
#                 return pydantic_object.model_construct()
#             return pydantic_object()
#         raise


# v3
"""
Utility for calling LLMs with error handling and retries.
"""

import logging
import os
from typing import Dict, Optional, Any, TypeVar, Type

from langchain.prompts import ChatPromptTemplate
from packages.framework.chat_model.get_chat_model import get_chat_model
from packages.framework.utils.with_retries import with_retries

logger = logging.getLogger(__name__)

# Get model parameters from environment
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.1"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2048"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

# Get the model - lazy initialization to allow credential checks first
LLM = None

def get_llm():
    """Get the LLM, initializing it if needed."""
    global LLM
    if LLM is None:
        try:
            LLM = get_chat_model(
                model_name=MODEL_NAME,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
                max_retries=MAX_RETRIES
            )
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {str(e)}")
            raise
    return LLM

T = TypeVar('T')

@with_retries(max_retries=MAX_RETRIES)
def call_llm(
    prompt_template: ChatPromptTemplate,
    input_parameters: Optional[Dict[str, Any]] = None,
    pydantic_object: Optional[Type[T]] = None
) -> Any:
    """
    Call an LLM with the given prompt and parameters.
    
    Args:
        prompt_template: The prompt template to use
        input_parameters: Parameters for the prompt
        pydantic_object: Optional Pydantic class for parsing the response
        
    Returns:
        Any: The LLM response, parsed if pydantic_object is provided
    """
    from packages.framework.utils.generic_chain import create_generic_chain
    
    logger.debug(f"Calling LLM with template: {prompt_template}")
    
    # Default empty parameters
    params = input_parameters or {}
    
    try:
        # Get the model and create the chain
        model = get_llm()
        chain = create_generic_chain(
            chat_model=model,
            template=prompt_template.template,
            pydantic_class=pydantic_object,
            **params
        )
        
        # Execute the chain
        result = chain.invoke({})
        
        # Return the result
        return result
    except Exception as e:
        logger.error(f"Error calling LLM: {str(e)}")
        # If we're expecting a Pydantic object, return a default instance
        if pydantic_object:
            logger.info("Returning default Pydantic object due to LLM error")
            # Create a default instance with required fields
            if hasattr(pydantic_object, 'model_construct'):
                # For ExtractedConditions, explicitly create with empty conditions list
                if pydantic_object.__name__ == 'ExtractedConditions':
                    logger.info("Creating ExtractedConditions with empty conditions list")
                    # Try both ways to handle different Pydantic versions
                    try:
                        return pydantic_object(conditions=[])
                    except:
                        return {"conditions": []}
                return pydantic_object.model_construct()
            return pydantic_object()
        raise