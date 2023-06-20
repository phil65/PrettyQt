from __future__ import annotations

from collections import defaultdict
from datetime import timedelta
import inspect
import itertools
import logging
import re
import types
import typing

logger = logging.getLogger(__name__)


TIME_REGEX = re.compile(
    r"((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?"
    r"((?P<seconds>\d+?)s)?((?P<milliseconds>\d+?)ms)?"
)

CASE_PATTERN = re.compile(r"(?<!^)(?=[A-Z])")


# def add_docs(klass):
#     import pathlib
#     from prettyqt import paths
#     klass_name = klass.__name__
#     qclass = klass
#     for k in klass.mro():
#         if k.__name__.startswith("Q"):
#             qclass = k
#             break
#     module = k.__module__.split(".")[1]
#     path = paths.DOCSTRING_PATH /  module
#     filepath = path / f"Q{klass_name.replace('Mixin', '')}.txt"
#     if filepath.exists():
#         klass.__doc__ =  filepath.read_text()
#     return klass


def is_in_slice(a_slice: slice | range, idx: int):
    """Note: this always returns False for negative slice.stop."""
    start = a_slice.start or 0
    is_behind_range = a_slice.stop is not None and idx >= a_slice.stop
    if idx < start or is_behind_range:
        return False
    step = a_slice.step or 1
    return (idx - start) % step == 0


def is_position_in_index(x: int, y: int, index) -> bool:
    """Index is a slice tuple."""
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


def find_common_ancestor(cls_list: list[type]) -> type:
    mros = [list(inspect.getmro(cls)) for cls in cls_list]
    track = defaultdict(int)
    while mros:
        for mro in mros:
            cur = mro.pop(0)
            track[cur] += 1
            if (
                track[cur] >= len(cls_list)
                and not cur.__name__.endswith("Mixin")
                and cur.__name__.startswith("Q")
            ):
                return cur
            if len(mro) == 0:
                mros.remove(mro)
    raise TypeError("Couldnt find common base class")


def yield_positions(
    rows: int | slice, columns: int | slice, num_rows: int, num_columns: int
) -> typing.Iterator[tuple[int, int]]:
    """Yields all x-y pairs for given row/column indexers.

    If indexer is slice without a defined stop, num_rows/num_columns is used for capping.
    """
    match (rows, columns):
        case slice() as row, slice() as col:
            rowcount = num_rows if row.stop is None else row.stop
            colcount = num_columns if col.stop is None else col.stop
            yield from itertools.product(range(rowcount)[row], range(colcount)[col])
        case slice() as row, int() as col:
            count = num_rows if row.stop is None else row.stop
            for i in range(count)[row]:
                yield (i, col)
        case int() as row, slice() as col:
            count = num_columns if col.stop is None else col.stop
            for i in range(count)[col]:
                yield (row, i)
        case int() as row, int() as col:
            yield (row, col)
        case _:
            raise TypeError((rows, columns))


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
    parts = TIME_REGEX.match(time_str)
    if not parts:
        raise ValueError(time_str)
    dct = parts.groupdict()
    time_params = {name: int(param) for (name, param) in dct.items() if param}
    secs = timedelta(**time_params).total_seconds()
    return int(secs * 1000)


def to_lower_camel(snake_str: str) -> str:
    # do nothing if nothing to camel
    if "_" not in snake_str:
        return snake_str
    first, *others = snake_str.split("_")
    return "".join([first.lower(), *map(str.title, others)])


def to_snake(camel_string: str) -> str:
    #  don´t snake-case snakes.
    if "_" in camel_string:
        return camel_string
    return CASE_PATTERN.sub("_", camel_string).lower()


def string_to_num_array(array: str) -> list[float]:
    floats = [float(i) for i in array.split(",")]
    return [int(i) if i.is_integer() else i for i in floats]


def get_color_percentage(
    color_1: tuple, color_2: tuple, percent: float
) -> tuple:
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
    ls = [
        round(color_1[i] + (color_2[i] - color_1[i]) * percent / 100)
        for i, _ in enumerate(color_1)
    ]
    return tuple(ls)


def get_subclasses(klass, include_abstract: bool = False):
    for i in klass.__subclasses__():
        yield from get_subclasses(i)
        if include_abstract or not inspect.isabstract(i):
            yield i


T = typing.TypeVar("T", bound=type)


def get_class_for_id(base_class: T, id_: str) -> T:
    base_classes = (
        typing.get_args(base_class)
        if isinstance(base_class, types.UnionType)
        else (base_class,)
    )
    for base_class in base_classes:
        for Klass in get_subclasses(base_class):
            if "ID" in Klass.__dict__ and Klass.ID == id_:
                logger.debug(f"found class for id {Klass.ID!r}")
                return Klass
    raise ValueError(f"Couldnt find class with id {id_!r} for base class {base_class}")


def get_module_classes(module: types.ModuleType) -> list[type]:
    clsmembers = inspect.getmembers(module, inspect.isclass)
    return [tpl[1] for tpl in clsmembers]


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
