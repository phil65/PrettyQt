"""Module containing helper functions."""

from __future__ import annotations

import enum
import functools
import logging
import operator

from typing import Any, TypeVar, TYPE_CHECKING

import bidict as bdct

if TYPE_CHECKING:
    from collections.abc import Iterable


logger = logging.getLogger(__name__)

KT = TypeVar("KT", bound=str)
VT = TypeVar("VT", bound=enum.Enum)


class bidict(bdct.bidict[KT, VT]):  # noqa: N801
    def __init__(self, *args, **kwargs):
        match args:
            case (dict(),):
                super().__init__(args[0])
            case _:
                super().__init__(kwargs)

    def __getitem__(self, item) -> VT:
        try:
            return super().__getitem__(item)
        except KeyError as e:
            raise InvalidParamError(item, list(self.keys())) from e

    def get_list(self, flag: enum.Enum) -> list[KT]:
        return [k for k, v in self.items() if v & flag]

    def get_dict(self, flag: enum.Enum) -> dict[KT, VT]:
        return {k: v & flag for k, v in self.items()}

    # def get_flag(self, **kwargs) -> dict[str, Any]:
    #     for k, v in kwargs.items():
    #     if isinstance(flag, enum.Enum):
    #         flag = flag.value
    #     return {k: v & flag for k, v in self.items()}

    def merge_flags(self, flags: Iterable[KT]) -> VT:
        return functools.reduce(operator.ior, [self[t] for t in flags])

    def get_enum_value(self, value: KT | VT) -> VT:
        return self[value] if isinstance(value, str) else value

    def get_str_value(self, value: KT | VT) -> KT:
        return value if isinstance(value, str) else self.inverse[value]


class InvalidParamError(ValueError):
    """Exception raised for invalid params in method calls.

    Args:
        value: param value which caused the error
        valid_options: allowed options
    """

    def __init__(self, value: Any, valid_options: Iterable):
        self.value = value
        opts = " / ".join(repr(opt) for opt in valid_options)
        self.message = f"Invalid value: {value!r}. Allowed options are {opts}."
        super().__init__(self.message)


def get_repr(_obj: Any, *args: Any, **kwargs: Any) -> str:
    """Get a suitable __repr__ string for an object.

    Args:
        _obj: The object to get a repr for.
        *args: Arguments for the repr
        **kwargs: Keyword arguments for the repr
    """
    classname = type(_obj).__name__
    parts = [repr(val) for val in args]
    kw_parts = [f"{name}={val!r}" for name, val in kwargs.items()]
    return f"{classname}({', '.join(parts + kw_parts)})"
