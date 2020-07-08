# -*- coding: utf-8 -*-
"""
"""

import pathlib
from typing import Union

from qtpy import QtGui

from prettyqt import gui


QtGui.QPixmap.__bases__ = (gui.PaintDevice,)


class Pixmap(QtGui.QPixmap):
    @classmethod
    def from_file(cls, path: Union[pathlib.Path, str]):
        if isinstance(path, str):
            path = pathlib.Path(path)
        with path.open(mode="rb") as f:
            data = f.read()
        # Create widget
        pixmap = cls()
        pixmap.loadFromData(data)
        return pixmap
