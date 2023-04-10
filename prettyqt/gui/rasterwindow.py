from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtGui


class RasterWindow(gui.PaintDeviceWindowMixin, QtGui.QRasterWindow):
    pass


if __name__ == "__main__":
    app = gui.app()
