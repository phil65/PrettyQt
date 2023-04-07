from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtGui


class Bitmap(gui.PixmapMixin, QtGui.QBitmap):
    pass


if __name__ == "__main__":
    app = gui.app()
    image = Bitmap()
    bytes(image)
