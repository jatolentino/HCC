"""
Utility function for adding retry functionality to functions.
"""

import logging
import time
import signal
from functools import wraps
from typing import Optional

class TimeoutError(Exception):
    """Exception raised when a function times out."""
    pass

def timeout_handler(signum, frame):
    """Signal handler for timeout."""
    raise TimeoutError("Execution timed out")

def with_retries(max_retries: int = 3, timeout_seconds: Optional[int] = None):
    """
    Decorator that adds retry functionality to a function.
    
    Args:
        max_retries: Maximum number of retry attempts
        timeout_seconds: Optional timeout in seconds
        
    Returns:
        Callable: Decorated function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    # Set up timeout if specified
                    if timeout_seconds is not None:
                        signal.signal(signal.SIGALRM, timeout_handler)
                        signal.alarm(timeout_seconds)

                    try:
                        result = func(*args, **kwargs)
                        if timeout_seconds is not None:
                            signal.alarm(0)  # Disable alarm
                        return result
                    finally:
                        if timeout_seconds is not None:
                            signal.alarm(0)  # Ensure alarm is disabled

                except TimeoutError as te:
                    if attempt == max_retries - 1:
                        logging.error(
                            f"Failed after {max_retries} attempts due to timeout"
                        )
                        raise te
                    logging.warning(f"Attempt {attempt + 1} timed out. Retrying...")
                    time.sleep(1 * (attempt + 1))  # Exponential backoff

                except Exception as e:
                    if attempt == max_retries - 1:  # Last attempt
                        logging.error(
                            f"Failed after {max_retries} attempts. Final error: {str(e)}"
                        )
                        raise e

                    logging.warning(
                        f"Attempt {attempt + 1} failed: {str(e)}. Retrying..."
                    )
                    time.sleep(1 * (attempt + 1))  # Exponential backoff

            raise Exception(f"Max retries ({max_retries}) reached")

        return wrapper

    return decorator