from __future__ import annotations

from datetime import timedelta
import re


REGEX = re.compile(
    r"((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?"
    r"((?P<seconds>\d+?)s)?((?P<milliseconds>\d+?)ms)?"
)


def dump_json(data: str):
    try:
        import orjson

        opts = orjson.OPT_NAIVE_UTC | orjson.OPT_SERIALIZE_NUMPY
        return orjson.dumps(data, option=opts)
    except ImportError:
        import json

        return json.dumps(data).encode()


def load_json(data):
    try:
        import orjson

        return orjson.loads(data)
    except ImportError:
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


def string_to_num_array(array: str) -> list[float]:
    floats = [float(i) for i in array.split(",")]
    return [int(i) if i.is_integer() else i for i in floats]


def cut_off_str(obj, max_len: int) -> str:
    """Create a string representation of an object, no longer than max_len characters.

    Uses repr(obj) to create the string representation. If this is longer than max_len -3
    characters, the last three will be replaced with elipsis.
    """
    s = repr(obj)
    return f"{s[:max_len - 3]}..." if len(s) > max_len - 3 else s


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
