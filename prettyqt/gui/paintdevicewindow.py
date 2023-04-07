from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtGui


class PaintDeviceWindowMixin(gui.WindowMixin, gui.PaintDeviceMixin):
    pass


class PaintDeviceWindow(PaintDeviceWindowMixin, QtGui.QPaintDeviceWindow):
    pass


if __name__ == "__main__":
    window = PaintDeviceWindow()
