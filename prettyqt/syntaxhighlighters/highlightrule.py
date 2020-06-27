# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""
# see https://github.com/ITVRoC/SeekurJr/blob/master/seekur_12.04/packages/
# multimaster_fkie/node_manager_fkie/src/node_manager_fkie/yaml_highlighter.py

from dataclasses import dataclass
import regex as re
from prettyqt import gui


@dataclass
class HighlightRule(object):
    regex = ""
    color = "black"
    italic = False
    bold = False
    minimal = False
    font_size = None
    nth = 0

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if isinstance(cls.regex, str):
            cls.compiled = re.compile(cls.regex)
            # cls.compiled.setMinimal(True)
        else:
            cls.compiled = [re.compile(r) for r in cls.regex]
        cls.format = cls.get_format()

    @classmethod
    def get_format(cls):
        fmt = gui.TextCharFormat()
        fmt.setFontItalic(cls.italic)
        fmt.set_foreground_color(cls.color)
        if cls.font_size:
            fmt.setFontPointSize(cls.font_size)
        if cls.bold:
            fmt.set_font_weight("bold")
        return fmt
