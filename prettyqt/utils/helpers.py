# -*- coding: utf-8 -*-

from typing import Dict, Any
from typing import List
import warnings
import functools
import sys
import operator


def string_to_num_array(array: str) -> List[float]:
    floats = [float(i) for i in array.split(",")]
    return [int(i) if i.is_integer() else i for i in floats]


def merge_flags(flags, mapping):
    return functools.reduce(operator.ior, [mapping[t] for t in flags])


def format_kwargs(kwargs: Dict[str, Any]) -> str:
    kwarg_list = [f"{k}={repr(v)}" for k, v in kwargs.items()]
    return ", ".join(kwarg_list)


def cut_off_str(obj, max_len: int):
    """Create a string representation of an object, no longer than max_len characters.

    Uses repr(obj) to create the string representation. If this is longer than max_len -3
    characters, the last three will be replaced with elipsis.
    """
    s = repr(obj)
    if len(s) > max_len - 3:
        s = s[: max_len - 3] + "..."
    return s


def deprecated(func):
    """A decorator which can be used to mark functions as deprecated.

    It will result in a warning being emitted when the function is used.
    """

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter("always", DeprecationWarning)  # turn off filter
        warnings.warn(
            "Call to deprecated function {}.".format(func.__name__),
            category=DeprecationWarning,
            stacklevel=2,
        )
        warnings.simplefilter("default", DeprecationWarning)  # reset filter
        return func(*args, **kwargs)

    return new_func


def is_dark_mode() -> bool:
    if sys.platform.startswith("win"):
        from prettyqt import core

        p = (
            "HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\"
            "Themes\\Personalize"
        )
        s = core.Settings(p, core.Settings.NativeFormat)
        return s.value("AppsUseLightTheme") == 0
    elif sys.platform == "darwin":
        import darkdetect

        return darkdetect.isDark()
    else:
        return False
