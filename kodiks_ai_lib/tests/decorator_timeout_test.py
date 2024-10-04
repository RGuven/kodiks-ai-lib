import time

import pytest
from loguru import logger

from ..decorators.timeout import TimeoutException, timeout  # type: ignore


@timeout(seconds=3)
def multiply_numbers(a, b, delay=0):
    """Function to multiply two numbers with an optional delay."""
    time.sleep(delay)
    return a * b


def test_multiply_numbers_success():
    """Test that function completes before timeout."""
    result = multiply_numbers(5, 10, delay=2)
    assert result == 50
    logger.info("test_multiply_numbers_success passed")


def test_multiply_numbers_timeout():
    """Test that function raises TimeoutException when delayed too long."""
    with pytest.raises(TimeoutException):
        multiply_numbers(5, 10, delay=5)
    logger.info("test_multiply_numbers_timeout passed")


def test_multiply_numbers_no_delay():
    """Test that function works with no delay."""
    result = multiply_numbers(2, 3)
    assert result == 6
    logger.info("test_multiply_numbers_no_delay passed")


def test_custom_timeout_exception():
    """Test custom timeout exception message."""
    with pytest.raises(TimeoutException, match="Custom timeout message"):

        @timeout(seconds=1, error_message="Custom timeout message")
        def delayed_function():
            time.sleep(2)

        delayed_function()
    logger.info("test_custom_timeout_exception passed")
