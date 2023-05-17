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


def to_lower_camel(snake_str: str) -> str:
    if "_" not in snake_str:
        return snake_str
    first, *others = snake_str.split("_")
    return "".join([first.lower(), *map(str.title, others)])


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


ANSI_STYLES = {
    1: {"font_weight": "bold"},
    2: {"font_weight": "lighter"},
    3: {"font_weight": "italic"},
    4: {"text_decoration": "underline"},
    5: {"text_decoration": "blink"},
    6: {"text_decoration": "blink"},
    8: {"visibility": "hidden"},
    9: {"text_decoration": "line-through"},
    30: {"color": "black"},
    31: {"color": "red"},
    32: {"color": "green"},
    33: {"color": "yellow"},
    34: {"color": "blue"},
    35: {"color": "magenta"},
    36: {"color": "cyan"},
    37: {"color": "white"},
}


def ansi2html(ansi_string: str, styles: dict[int, dict[str, str]] = ANSI_STYLES) -> str:
    """Convert ansi string to colored HTML.

    Arguments:
        ansi_string:
            text with ANSI color codes.
        styles:
            A mapping from ANSI codes to a dict of css kwargs:values,
            by default ANSI_STYLES

    Returns:
        HTML string
    """
    previous_end = 0
    in_span = False
    ansi_codes = []
    ansi_finder = re.compile("\033\\[([\\d;]*)([a-zA-z])")
    parts = []
    for match in ansi_finder.finditer(ansi_string):
        parts.append(ansi_string[previous_end : match.start()])
        previous_end = match.end()
        params, command = match.groups()

        if command not in "mM":
            continue

        try:
            params = [int(p) for p in params.split(";")]
        except ValueError:
            params = [0]

        for i, v in enumerate(params):
            if v == 0:
                params = params[i + 1 :]
                if in_span:
                    in_span = False
                    parts.append("</span>")
                ansi_codes = []
                if not params:
                    continue

        ansi_codes.extend(params)
        if in_span:
            parts.append("</span>")
            in_span = False

        if not ansi_codes:
            continue

        style = [
            "; ".join([f"{k}: {v}" for k, v in styles[k].items()]).strip()
            for k in ansi_codes
            if k in styles
        ]
        parts.append(f'<span style="{"; ".join(style)}">')

        in_span = True

    parts.append(ansi_string[previous_end:])
    if in_span:
        parts.append("</span>")
        in_span = False
    return "".join(parts)
