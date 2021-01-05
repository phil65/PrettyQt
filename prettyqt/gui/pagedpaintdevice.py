from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtGui


QtGui.QPagedPaintDevice.__bases__ = (gui.PaintDevice,)


class PagedPaintDevice(QtGui.QPagedPaintDevice):
    pass


if __name__ == "__main__":
    device = PagedPaintDevice()
