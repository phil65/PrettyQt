"""Module containing helper functions."""

from collections.abc import Iterable
import logging
from typing import Any

import bidict as bdct


logger = logging.getLogger(__name__)


class bidict(bdct.bidict):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            super().__init__(args[0])
        else:
            super().__init__(kwargs)


class InvalidParamError(ValueError):
    """Exception raised for invalid params in method calls.

    Args:
        value: param value which caused the error
        valid_options: allowed options
    """

    def __init__(self, value, valid_options: Iterable):
        self.value = value
        opts = " / ".join(repr(opt) for opt in valid_options)
        self.message = f"Invalid value: {value!r}. Allowed options are {opts}."
        super().__init__(self.message)


def get_repr(obj: Any, *args, **kwargs: Any) -> str:
    """Get a suitable __repr__ string for an object.

    Args:
        obj: The object to get a repr for.
        *args: Arguments for the repr
        **kwargs: Keyword arguments for the repr
    """
    classname = type(obj).__name__
    parts = [repr(val) for val in args]
    kw_parts = [f"{name}={val!r}" for name, val in kwargs.items()]
    return f"{classname}({', '.join(parts + kw_parts)})"
