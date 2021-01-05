from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtGui


QtGui.QRasterWindow.__bases__ = (gui.PaintDeviceWindow,)


class RasterWindow(QtGui.QRasterWindow):
    pass


if __name__ == "__main__":
    app = gui.GuiApplication([])
