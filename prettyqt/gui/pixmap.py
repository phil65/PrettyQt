# -*- coding: utf-8 -*-

import pathlib
from typing import Union

from qtpy import QtGui, QtCore

from prettyqt import gui, core


QtGui.QPixmap.__bases__ = (gui.PaintDevice,)


class Pixmap(QtGui.QPixmap):
    def __bool__(self):
        return not self.isNull()

    def __getstate__(self):
        return core.DataStream.create_bytearray(self)

    def __setstate__(self, ba):
        self.__init__()
        core.DataStream.write_bytearray(ba, self)

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

    @classmethod
    def create_dot(cls, color="black", size=16):
        col = gui.Color(color)
        px = cls(size, size)
        px.fill(QtCore.Qt.transparent)
        px_size = px.rect().adjusted(1, 1, -1, -1)
        with gui.Painter(px) as painter:
            painter.use_antialiasing()
            painter.setBrush(col)
            painter.set_pen(color=gui.Color(15, 15, 15), width=1.25)
            painter.drawEllipse(px_size)
        return px


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    p = Pixmap()
    print(bool(p))
