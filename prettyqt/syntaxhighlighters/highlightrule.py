# see https://github.com/ITVRoC/SeekurJr/blob/master/seekur_12.04/packages/
# multimaster_fkie/node_manager_fkie/src/node_manager_fkie/yaml_highlighter.py

import re
from typing import TYPE_CHECKING, ClassVar

from prettyqt import gui


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


class HighlightRule:
    """A highlighting rule, configured via class attributes of subclasses."""

    regex: ClassVar[str | list[str]] = ""
    color: ClassVar[datatypes.ColorType] = "black"
    italic: ClassVar[bool] = False
    bold: ClassVar[bool] = False
    minimal: ClassVar[bool] = False
    font_size: ClassVar[float | None] = None
    nth: ClassVar[int] = 0
    compiled: ClassVar[re.Pattern | list[re.Pattern] | None] = None
    fmt: ClassVar[gui.TextCharFormat]

    def __init_subclass__(cls):
        super().__init_subclass__()
        if isinstance(cls.regex, str):
            cls.compiled = re.compile(cls.regex)
            # cls.compiled.setMinimal(True)
        else:
            cls.compiled = [re.compile(r) for r in cls.regex]
        cls.fmt = cls.get_format()

    @classmethod
    def get_format(cls) -> gui.TextCharFormat:
        fmt = gui.TextCharFormat()
        fmt.setFontItalic(cls.italic)
        fmt.set_foreground_color(cls.color)
        if cls.font_size:
            fmt.setFontPointSize(cls.font_size)
        if cls.bold:
            fmt.set_font_weight("bold")
        return fmt
