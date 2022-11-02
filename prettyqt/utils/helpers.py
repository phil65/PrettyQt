from __future__ import annotations

from collections.abc import Mapping
from datetime import timedelta
import functools
import operator
import re
import sys
from typing import Any


REGEX = re.compile(
    r"((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?"
    r"((?P<seconds>\d+?)s)?((?P<milliseconds>\d+?)ms)?"
)


def dump_json(data: str):
    try:
        import orjson

        OPTS = orjson.OPT_NAIVE_UTC | orjson.OPT_SERIALIZE_NUMPY
        return orjson.dumps(data, option=OPTS)
    except (ImportError, ModuleNotFoundError):
        import json

        return json.dumps(data).encode()


def load_json(data):
    try:
        import orjson

        return orjson.loads(data)
    except (ImportError, ModuleNotFoundError):
        import json

        return json.loads(data)


def parse_time(time_str: str) -> int:
    parts = REGEX.match(time_str)
    if not parts:
        raise ValueError(time_str)
    dct = parts.groupdict()
    time_params = {name: int(param) for (name, param) in dct.items() if param}
    secs = timedelta(**time_params).total_seconds()
    return int(secs * 1000)


def format_seconds(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:02}:{h:02}:{h:02}"


def string_to_num_array(array: str) -> list[float]:
    floats = [float(i) for i in array.split(",")]
    return [int(i) if i.is_integer() else i for i in floats]


def merge_flags(flags, mapping: Mapping):
    return functools.reduce(operator.ior, [mapping[t] for t in flags])


def format_kwargs(kwargs: dict[str, Any]) -> str:
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


def get_color_percentage(
    color_1: tuple[int, int, int, int], color_2: tuple[int, int, int, int], percent: float
) -> tuple[int, int, int, int]:
    """Get a color which is percent% interpolated between start and end.

    Args:
        color_1 : Start color components (R, G, B, A / H, S, V, A / H, S, L, A)
        color_2 : End color components (R, G, B, A / H, S, V, A / H, S, L, A)
        percent: Percentage to interpolate, 0-100.
                 0: Start color will be returned.
                 100: End color will be returned.

    Return:
        A (x, y, z, alpha) tuple with the interpolated color components.
    """
    if not 0 <= percent <= 100:
        raise ValueError("percent needs to be between 0 and 100!")
    x = round(color_1[0] + (color_2[0] - color_1[0]) * percent / 100)
    y = round(color_1[1] + (color_2[1] - color_1[1]) * percent / 100)
    z = round(color_1[2] + (color_2[2] - color_1[2]) * percent / 100)
    a = round(color_1[3] + (color_2[3] - color_1[3]) * percent / 100)
    return (x, y, z, a)


def is_dark_mode() -> bool:
    if sys.platform.startswith("win"):
        from prettyqt import core

        path = (
            "HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\"
            "Themes\\Personalize"
        )
        settings = core.Settings(path, core.Settings.Format.NativeFormat)
        return settings.value("AppsUseLightTheme") == 0
    elif sys.platform == "darwin":
        import darkdetect

        return darkdetect.isDark()
    else:
        return False
