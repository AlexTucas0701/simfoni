from functools import wraps
from typing import Callable

from pydantic_core import (
    ValidationError,
)  # Used to catch validation errors from Pydantic
from rest_framework.response import Response  # DRF response for API endpoints

from config import Config
from utils.exceptions import MaxRetryExceedException  # Custom exception for retry limit


# Decorator to handle Pydantic validation errors and return them in the API response
def pydantic_exception_handler(status=400):
    def real_decorator(func: Callable):
        @wraps(func)  # Preserve original function signature and attributes
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)  # Execute the wrapped function
            except ValidationError as e:  # Catch Pydantic validation errors
                errors = {}
                # Loop through the validation errors to collect field-specific messages
                for validation_error in e.errors():
                    # Extract error message and assign to the field name (location)
                    errors[validation_error["loc"][0]] = validation_error["msg"]
                # Return error response with the validation error details and HTTP 400 status
                return Response(errors, status=status)

        return wrapper

    return real_decorator


# Decorator to handle the custom MaxRetryExceedException and return a 429 status
def max_retry_exceed_exception_handler(status=429):
    def real_decorator(func: Callable):
        @wraps(func)  # Preserve original function signature and attributes
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)  # Execute the wrapped function
            except MaxRetryExceedException:
                # Return a 429 response indicating that the user should try again later
                return Response(
                    {
                        "error": "Try again after a while",  # User-friendly error message
                    },
                    status=status,  # HTTP status 429 (Too Many Requests)
                )

        return wrapper

    return real_decorator


def unknow_exception_handler(status=500):
    def real_decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                white_box_error_description = str(e)
                black_box_error_description = "Unknown exception occured. "
                "Please enables dev stage to see"
                description = (
                    white_box_error_description
                    if Config.DEV_STAGE
                    else black_box_error_description
                )
                return Response(
                    {
                        "error": description,
                    },
                    status=status,
                )

        return wrapper

    return real_decorator
