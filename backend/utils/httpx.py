from functools import wraps
from typing import Callable

from pydantic_core import ValidationError
from rest_framework.response import Response


def pydantic_exception_handler(status=400):
    def real_decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValidationError as e:
                errors = {}
                for validation_error in e.errors():
                    errors[validation_error["loc"][0]] = validation_error["msg"]
                return Response(errors, status=status)

        return wrapper

    return real_decorator
