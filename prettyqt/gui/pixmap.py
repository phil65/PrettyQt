# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import pathlib

from qtpy import QtGui


class Pixmap(QtGui.QPixmap):

    @classmethod
    def from_file(cls, path: pathlib.Path):
        with path.open(mode="rb") as f:
            data = f.read()
        # Create widget
        pixmap = cls()
        pixmap.loadFromData(data)
        return pixmap
