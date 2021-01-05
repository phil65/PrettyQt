from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtGui


QtGui.QPaintDeviceWindow.__bases__ = (gui.Window, gui.PaintDevice)


class PaintDeviceWindow(QtGui.QPaintDeviceWindow):
    pass


if __name__ == "__main__":
    window = PaintDeviceWindow()
