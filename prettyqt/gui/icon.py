# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import pathlib

from qtpy import QtGui
import qtawesome as qta

from prettyqt import gui


class Icon(QtGui.QIcon):

    def __init__(self, icon=None):
        if isinstance(icon, pathlib.Path):
            icon = str(icon)
        super().__init__(icon)

    @classmethod
    def for_color(cls, color: str):
        color = gui.Color.from_text(color)
        if color.isValid():
            bitmap = gui.Pixmap(16, 16)
            bitmap.fill(color)
            icon = gui.Icon(bitmap)
        else:
            icon = qta.icon("mdi.card-outline")
        return icon


if __name__ == "__main__":
    icon = Icon()
