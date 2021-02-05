# see https://github.com/ITVRoC/SeekurJr/blob/master/seekur_12.04/packages/
# multimaster_fkie/node_manager_fkie/src/node_manager_fkie/yaml_highlighter.py

from __future__ import annotations

from dataclasses import dataclass

import regex as re

from prettyqt import gui


@dataclass
class HighlightRule:
    regex: str | list[str] = ""
    color: str = "black"
    italic: bool = False
    bold: bool = False
    minimal: bool = False
    font_size: float | None = None
    nth: int = 0
    compiled = None
    fmt: gui.TextCharFormat = gui.TextCharFormat()

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
