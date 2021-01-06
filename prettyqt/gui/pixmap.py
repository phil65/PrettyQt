from __future__ import annotations

import os
import pathlib
from typing import Union

from prettyqt import core, gui
from prettyqt.qt import QtCore, QtGui


QtGui.QPixmap.__bases__ = (gui.PaintDevice,)


class Pixmap(QtGui.QPixmap):
    def __bool__(self):
        return not self.isNull()

    def __getstate__(self):
        return bytes(self)

    def __setstate__(self, ba):
        core.DataStream.write_bytearray(ba, self)

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return bytes(ba)

    def __eq__(self, other):
        if not isinstance(other, Pixmap):
            return False
        # return bytes(self) == bytes(other)
        return self.toImage() == other.toImage()

    def __hash__(self):
        return self.cacheKey()

    @classmethod
    def from_file(cls, path: Union[os.PathLike, str]) -> Pixmap:
        path = pathlib.Path(path)
        with path.open(mode="rb") as f:
            data = f.read()
        # Create widget
        pixmap = cls()
        pixmap.loadFromData(QtCore.QByteArray(data))
        return pixmap

    def get_size(self) -> core.Size:
        return core.Size(self.size())

    def get_rect(self) -> core.Rect:
        return core.Rect(self.rect())

    def to_image(self) -> gui.Image:
        return gui.Image(self.toImage())

    @classmethod
    def create_dot(cls, color="black", size: int = 16) -> Pixmap:
        col = gui.Color(color)
        px = cls(size, size)
        px.fill(QtCore.Qt.transparent)
        px_size = px.rect().adjusted(1, 1, -1, -1)
        with gui.Painter(px) as painter:
            painter.use_antialiasing()
            painter.setBrush(col)
            painter.set_pen(color=gui.Color(15, 15, 15), width=1)
            painter.drawEllipse(px_size)
        return px


if __name__ == "__main__":
    from prettyqt import gui

    app = gui.app()
    p = Pixmap()
    print(bytes(p))
