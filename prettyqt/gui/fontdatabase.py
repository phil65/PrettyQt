# -*- coding: utf-8 -*-
"""
"""

import logging
from typing import Union
import pathlib

from qtpy import QtGui

from prettyqt.utils import bidict

logger = logging.getLogger(__name__)

SYSTEM_FONTS = bidict(
    general=QtGui.QFontDatabase.GeneralFont,
    fixed=QtGui.QFontDatabase.FixedFont,
    title=QtGui.QFontDatabase.TitleFont,
    smallest_readable=QtGui.QFontDatabase.SmallestReadableFont,
)


class FontDatabase(QtGui.QFontDatabase):
    def add_fonts_from_folder(self, path: Union[str, pathlib.Path]):
        for p in path.iterdir():
            if p.suffix.lower() in [".ttf", ".otf"]:
                logger.debug(f"adding font {p} to database.")
                self.addApplicationFont(str(p))

    def get_system_font(self, font_type: str):
        if font_type not in SYSTEM_FONTS:
            raise ValueError(f"Invalid font type '{font_type}'")
        return self.systemFont(SYSTEM_FONTS[font_type])
