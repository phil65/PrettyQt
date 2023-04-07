from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtGui


class PagedPaintDeviceMixin(gui.PaintDeviceMixin):
    pass


class PagedPaintDevice(PagedPaintDeviceMixin, QtGui.QPagedPaintDevice):
    pass


if __name__ == "__main__":
    device = PagedPaintDevice()
