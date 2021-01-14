from __future__ import annotations

from datetime import timedelta
import functools
import operator
import re
import sys
from typing import Any, Dict, List, Mapping


REGEX = re.compile(
    r"((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?"
    r"((?P<seconds>\d+?)s)?((?P<milliseconds>\d+?)ms)?"
)


def parse_time(time_str: str) -> int:
    parts = REGEX.match(time_str)
    if not parts:
        raise ValueError(time_str)
    dct = parts.groupdict()
    time_params = {name: int(param) for (name, param) in dct.items() if param}
    secs = timedelta(**time_params).total_seconds()
    return int(secs * 1000)


def string_to_num_array(array: str) -> List[float]:
    floats = [float(i) for i in array.split(",")]
    return [int(i) if i.is_integer() else i for i in floats]


def merge_flags(flags, mapping: Mapping):
    return functools.reduce(operator.ior, [mapping[t] for t in flags])


def format_kwargs(kwargs: Dict[str, Any]) -> str:
    kwarg_list = [f"{k}={repr(v)}" for k, v in kwargs.items()]
    return ", ".join(kwarg_list)


def cut_off_str(obj, max_len: int) -> str:
    """Create a string representation of an object, no longer than max_len characters.

    Uses repr(obj) to create the string representation. If this is longer than max_len -3
    characters, the last three will be replaced with elipsis.
    """
    s = repr(obj)
    if len(s) > max_len - 3:
        return s[: max_len - 3] + "..."
    return s


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
