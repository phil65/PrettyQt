# -*- coding: utf-8 -*-
"""
"""

import pathlib


import qtawesome as qta
from qtpy import QtCore, QtGui

from prettyqt import core, gui


class Icon(QtGui.QIcon):
    def __init__(self, icon=None):
        if isinstance(icon, pathlib.Path):
            icon = str(icon)
        super().__init__(icon)

    # def __reduce__(self):
    #     return type(self), (), self.__getstate__()

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __bool__(self):
        return not bool(self.isNull())

    def __getstate__(self):
        ba = QtCore.QByteArray()
        stream = QtCore.QDataStream(ba, QtCore.QIODevice.WriteOnly)
        pixmap = self.pixmap(QtCore.QSize(256, 256))
        stream << pixmap
        return ba

    def __setstate__(self, ba):
        stream = QtCore.QDataStream(ba, QtCore.QIODevice.ReadOnly)
        px = QtGui.QPixmap()
        stream >> px
        super().__init__(px)

    @classmethod
    def by_name(cls, name: str) -> "Icon":
        return cls(qta.icon(name))

    @classmethod
    def for_color(cls, color_str: str) -> "Icon":
        color = gui.Color.from_text(color_str)
        if color.isValid():
            bitmap = gui.Pixmap(16, 16)
            bitmap.fill(color)
            icon = gui.Icon(bitmap)
        else:
            icon = cls(qta.icon("mdi.card-outline"))
        return icon

    def get_pixmap(self, size: int) -> QtGui.QPixmap:
        size = core.Size(size, size)
        return self.pixmap(size)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    icon = Icon.for_color("green")
