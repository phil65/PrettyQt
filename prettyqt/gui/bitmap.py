from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtGui


QtGui.QBitmap.__bases__ = (gui.Pixmap,)


class Bitmap(QtGui.QBitmap):
    pass


if __name__ == "__main__":
    app = gui.app()
    image = Bitmap()
    bytes(image)
