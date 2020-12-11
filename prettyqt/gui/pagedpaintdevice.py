from qtpy import QtGui

from prettyqt import gui


QtGui.QPagedPaintDevice.__bases__ = (gui.PaintDevice,)


class PagedPaintDevice(QtGui.QPagedPaintDevice):
    pass


if __name__ == "__main__":
    device = PagedPaintDevice()
