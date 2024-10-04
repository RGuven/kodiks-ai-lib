import signal
from functools import wraps


class TimeoutException(Exception):
    """Custom exception for handling timeout errors."""

    pass


def timeout(seconds=30, error_message="Timeout"):
    """Decorator to limit the execution time of a function.

    Args:
        seconds (int): Time limit for function execution.
        error_message (str): Custom error message for timeout.

    Raises:
        TimeoutException: If the function takes longer than `seconds` to complete.
    """

    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutException(error_message)

        @wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)  # Set the timeout
            try:
                return func(*args, **kwargs)
            finally:
                signal.alarm(0)  # Disable the alarm after the function completes

        return wrapper

    return decorator
