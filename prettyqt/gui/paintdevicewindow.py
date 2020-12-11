from qtpy import QtGui

from prettyqt import gui


QtGui.QPaintDeviceWindow.__bases__ = (gui.Window, gui.PaintDevice)


class PaintDeviceWindow(QtGui.QPaintDeviceWindow):
    pass


if __name__ == "__main__":
    window = PaintDeviceWindow()
