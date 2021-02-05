from __future__ import annotations

import os
import pathlib

from prettyqt import core, gui
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import colors, types


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
    def from_file(cls, path: os.PathLike | str) -> Pixmap:
        path = pathlib.Path(path)
        with path.open(mode="rb") as f:
            data = f.read()
        # Create widget
        pixmap = cls()
        pixmap.loadFromData(QtCore.QByteArray(data))
        return pixmap

    @classmethod
    def from_image(cls, img: QtGui.QImage, flags) -> Pixmap:
        return cls(cls.fromImage(img, flags))

    def get_size(self) -> core.Size:
        return core.Size(self.size())

    def get_rect(self) -> core.Rect:
        return core.Rect(self.rect())

    def to_image(self) -> gui.Image:
        return gui.Image(self.toImage())

    def rotated(self, rotation: int) -> Pixmap:
        w, h = self.width(), self.height()
        pixmap = self.transformed(gui.Transform().rotate(rotation))
        new_w, new_h = pixmap.width(), pixmap.height()
        return pixmap.copy((new_w - w) // 2, (new_h - h) // 2, w, h)

    @classmethod
    def create_dot(cls, color: types.ColorType = "black", size: int = 16) -> Pixmap:
        col = colors.get_color(color)
        px = cls(size, size)
        px.fill(QtCore.Qt.transparent)
        px_size = px.rect().adjusted(1, 1, -1, -1)
        with gui.Painter(px) as painter:
            painter.use_antialiasing()
            painter.setBrush(col)
            pen_color = gui.Color(15, 15, 15)
            painter.set_pen(color=pen_color, width=1)
            painter.drawEllipse(px_size)
        return px

    @classmethod
    def create_checkerboard_pattern(
        cls, n: int, color_1: types.ColorType, color_2: types.ColorType
    ):
        """Construct tileable checkerboard pattern for paint events."""
        # Brush will be an n×n checkerboard pattern
        pat = gui.Pixmap(2 * n, 2 * n)
        bg0 = colors.get_color(color_1)
        bg1 = colors.get_color(color_2)
        with gui.Painter(pat) as p:
            p.setPen(QtCore.Qt.NoPen)
            # Paint a checkerboard pattern for the color to be overlaid on
            p.fillRect(pat.rect(), bg0)
            p.fillRect(0, 0, n, n, bg1)
            p.fillRect(n, n, 2 * n, 2 * n, bg1)
        return pat


if __name__ == "__main__":
    from prettyqt import gui

    app = gui.app()
    p = Pixmap.create_checkerboard_pattern(100, "black", "white")
    print(bytes(p))
