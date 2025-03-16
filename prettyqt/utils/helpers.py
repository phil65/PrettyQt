from __future__ import annotations

import datetime
import itertools
import logging
import re
import typing


logger = logging.getLogger(__name__)


TIME_REGEX = re.compile(
    r"((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?"
    r"((?P<seconds>\d+?)s)?((?P<milliseconds>\d+?)ms)?"
)

CASE_PATTERN = re.compile(r"(?<!^)(?=[A-Z])")


def is_in_slice(a_slice: slice | range, idx: int) -> bool:
    """Check whether given index is part of given slice.

    Note: this always returns False for negative slice.stop.

    Arguments:
        a_slice: slice to check
        idx: index to check
    """
    start = a_slice.start or 0
    is_behind_range = a_slice.stop is not None and idx >= a_slice.stop
    if idx < start or is_behind_range:
        return False
    step = a_slice.step or 1
    return (idx - start) % step == 0


def is_position_in_index(x: int, y: int, index) -> bool:
    """Check whether given x and y values are part of the index.

    Arguments:
        x: x value
        y: y value
        index: tuple of two ints / slices. If None, True is returned.
    """
    match index:
        case None:
            return True
        case slice() as row, int() as col:
            return is_in_slice(row, x) and y == col
        case int() as row, slice() as col:
            return is_in_slice(col, y) and x == row
        case slice() as row, slice() as col:
            return is_in_slice(col, y) and is_in_slice(row, x)
        case int() as row, int() as col:
            return x == row and y == col
        case _:
            raise TypeError(index)


def iter_positions(
    rows: int | slice, columns: int | slice, num_rows: int, num_columns: int
) -> typing.Iterator[tuple[int, int]]:
    """Yields all x-y pairs for given row/column indexers.

    If indexer is slice without a defined stop, num_rows/num_columns is used for capping.
    """
    match (rows, columns):
        case slice() as rowslice, slice() as colslice:
            rowcount = num_rows if rowslice.stop is None else rowslice.stop
            colcount = num_columns if colslice.stop is None else colslice.stop
            yield from itertools.product(
                range(rowcount)[rowslice], range(colcount)[colslice]
            )
        case slice() as rowslice, int() as col:
            count = num_rows if rowslice.stop is None else rowslice.stop
            for i in range(count)[rowslice]:
                yield (i, col)
        case int() as row, slice() as colslice:
            count = num_columns if colslice.stop is None else colslice.stop
            for i in range(count)[colslice]:
                yield (row, i)
        case int() as row, int() as col:
            yield (row, col)
        case _:
            raise TypeError((rows, columns))


def get_connections(objects, child_getter, id_getter=None):
    items = set()
    connections = []

    def add_connections(item):
        identifier = id_getter(item) if id_getter else item
        if identifier not in items:
            # if item.__module__.startswith(base_module):
            items.add(identifier)
            for base in child_getter(item):
                connections.append((id_getter(base) if id_getter else base, identifier))
                add_connections(base)

    for obj in objects:
        add_connections(obj)
    return items, connections


def parse_time(time_str: str) -> int:
    """Parse given string and return duration in seconds.

    Arguments:
        time_str: String to parse
    """
    parts = TIME_REGEX.match(time_str)
    if not parts:
        raise ValueError(time_str)
    dct = parts.groupdict()
    time_params = {name: int(param) for (name, param) in dct.items() if param}
    secs = datetime.timedelta(**time_params).total_seconds()
    return int(secs * 1000)


def to_lower_camel(snake_str: str) -> str:
    # do nothing if nothing to camel
    if "_" not in snake_str:
        return snake_str
    first, *others = snake_str.split("_")
    return "".join([first.lower(), *map(str.title, others)])


def to_snake(camel_string: str) -> str:
    #  don't snake-case snakes.
    if "_" in camel_string:
        return camel_string
    return CASE_PATTERN.sub("_", camel_string).lower()


def string_to_num_array(array: str) -> list[float]:
    floats = [float(i) for i in array.split(",")]
    return [int(i) if i.is_integer() else i for i in floats]


def get_color_percentage(color_1: tuple, color_2: tuple, percent: float) -> tuple:
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
    if not 0 <= percent <= 100:  # noqa: PLR2004
        msg = "percent needs to be between 0 and 100!"
        raise ValueError(msg)
    ls = [
        round(color_1[i] + (color_2[i] - color_1[i]) * percent / 100)
        for i, _ in enumerate(color_1)
    ]
    return tuple(ls)


def call_and_append_until(
    caller: object,
    call: typing.Callable,
    condition: typing.Callable,
    append_caller: bool = True,
) -> list:
    ls = [caller] if append_caller else []
    child_elem = caller
    while condition(parent_elem := call(child_elem)):
        ls.append(parent_elem.index(child_elem))
        child_elem = parent_elem
    return ls


def move_in_list(ls: list, indexes: list[int], target_row: int) -> list:
    """Moves items with given indexes inside list ls to target row."""
    new = [ls[i] for i in indexes]
    in_range = target_row < len(ls) and target_row != -1
    pos = ls.index(ls[target_row]) if in_range else len(ls)
    rem = 0
    for i in sorted(indexes, reverse=True):
        ls.pop(i)
        if i <= pos:
            rem += 1
    for item in reversed(new):
        ls.insert(pos - rem, item)
    return ls


def format_name(name) -> str:
    if isinstance(name, tuple | list):
        return " | ".join(str(i) for i in name)
    return str(name)


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
    ansi_codes: list[int] = []
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
